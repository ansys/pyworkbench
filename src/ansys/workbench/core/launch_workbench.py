import logging
import os
import platform
import tempfile
import time
import uuid

try:
    if platform.system() == "Windows":
        import wmi
except ImportError:
    # Handle the case when 'wmi' cannot be imported
    wmi = None

from ansys.workbench.core.workbench_client import WorkbenchClient


class LaunchWorkbench:
    """Launch Workbench server on local or remote Windows machine and create a Workbench client that connects to the server."""  # noqa: E501

    def __init__(
        self,
        release="241",
        client_workdir=None,
        server_workdir=None,
        host=None,
        username=None,
        password=None,
    ):
        self._release = release
        self._host = host
        self._username = username
        self._password = password
        self._wmi_connection = None
        self._process_id = -1
        self._client = None

        if len(release) != 3 or not release.isdigit():
            raise Exception("invalid ANSYS release number: " + release)
        if client_workdir is None:
            client_workdir = tempfile.gettempdir()
        self.client_workdir = client_workdir
        port = self._launch_server(server_workdir)
        if port is not None and port > 0:
            if host is None:
                host = "localhost"
            self.client = WorkbenchClient(
                local_workdir=client_workdir, server_host=host, server_port=port
            )
            self.client.connect()

    def _launch_server(self, server_workdir=None):
        try:
            if self._host is None:
                self._wmi_connection = wmi.WMI()
            else:
                self._wmi_connection = wmi.WMI(
                    self._host, user=self._username, password=self._password
                )
            logging.info("host connection established")

            install_path = None
            for ev in self._wmi_connection.Win32_Environment():
                if ev.Name == "AWP_ROOT" + self._release:
                    install_path = ev.VariableValue
                    break
            if install_path is None:
                install_path = "C:/Program Files/Ansys Inc/v" + self._release
                logging.warning(
                    "ANSYS installation not found. Assume the default location: " + install_path
                )
            else:
                logging.info("ANSYS installation found at: " + install_path)
            executable = os.path.join(install_path, "Framework", "bin", "Win64", "RunWB2.exe")
            prefix = uuid.uuid4().hex
            workdir_arg = ""
            if server_workdir is not None:
                # use forward slash only to avoid escaping as command line argument
                server_workdir = server_workdir.replace("\\", "/")
                workdir_arg = ",WorkingDirectory='" + server_workdir + "'"
            command = (
                executable
                + " -I -E \"StartServer(EnvironmentPrefix='"
                + prefix
                + "'"
                + workdir_arg
                + ')"'
            )

            process_startup_info = self._wmi_connection.Win32_ProcessStartup.new(ShowWindow=1)
            process_id, result = self._wmi_connection.Win32_Process.Create(
                CommandLine=command, ProcessStartupInformation=process_startup_info
            )

            if result == 0:
                logging.info("Workbench launched on the host with process id: " + str(process_id))
                self._process_id = process_id
            else:
                logging.error("Workbench failed to launch on the host")
                return 0

            # retrieve server port once WB is fully up running
            port = None
            timeout = 60 * 8  # set 8 minutes as upper limit for WB startup
            start_time = time.time()
            while True:
                for ev in self._wmi_connection.Win32_Environment():
                    if ev.Name == "ANSYS_FRAMEWORK_SERVER_PORT":
                        port = ev.VariableValue
                        if port.startswith(prefix):
                            port = port[len(prefix) :]
                            break
                        else:
                            port = None
                        break
                if port is not None:
                    break
                if time.time() - start_time > timeout:
                    logging.error("Failed to start Workbench service within reasonable timeout")
                    break
                time.sleep(10)
            if port is None:
                logging.error("Failed to retrieve the port used by Workbench service")
            else:
                logging.info("Workbench service uses port " + port)

            return int(port)

        except wmi.x_wmi:
            logging.error("wrong credential")

    def exit(self):
        """Shutdown Workbench server and dispose the connected client.
        """
        if self.client is not None:
            self.client.disconnect()
            self.client = None

        if self._wmi_connection is None:
            return

        # collect parent-children mapping
        children = {self._process_id: []}
        process_by_id = {}
        for p in self._wmi_connection.Win32_Process():
            process_by_id[p.ProcessId] = p
            children.setdefault(p.ProcessId, [])
            if p.ParentProcessId is None:
                continue
            children.setdefault(p.ParentProcessId, [])
            children[p.ParentProcessId].append(p.ProcessId)

        # terminate related processes bottom-up
        toTerminate = []
        thisLevel = set([self._process_id])
        while True:
            nextLevel = set()
            for p in thisLevel:
                nextLevel.update(children[p])
            if len(nextLevel) == 0:
                break
            toTerminate.append(nextLevel)
            thisLevel = nextLevel
        for ps in reversed(toTerminate):
            for p in ps:
                logging.info("shutting down " + process_by_id[p].Name + " ...")
                try:
                    process_by_id[p].Terminate()
                except:
                    pass

        logging.info("Workbench server ended")
        self._wmi_connection = None
        self._process_id = -1

    def set_console_log_level(self, log_level):
        """Set log filter level for the client console.

        Parameters
        ----------
        log_level: str, optional
            level of logging. options are "debug", "info", "warning", "error", "critical"
            the default is "error".
        """
        self.client.set_console_log_level(log_level)

    def set_log_file(self, log_file):
        """Set a local log file for WB server log.

        Parameters
        ----------
        log_file: str
            path to a local file used for logging
        """
        self.client.set_log_file(log_file)

    def reset_log_file(self):
        """No longer use the current log file for WB server log.
        """
        self.client.reset_log_file()

    def run_script_string(self, script_string, log_level="error"):
        """Run the given script on the server.

        Parameters
        ----------
            script_string: str
                a string containing the content of the script to run
            log_level: str, optional
                level of logging. options are "debug", "info", "warning", "error", "critical"
                the default is "error".
        """
        return self.client.run_script_string(script_string, log_level)

    def run_script_file(self, script_file_name, log_level="error"):
        """Run the given script file on the server.

        Parameters
        ----------
            script_file_name: str
                file name of the script, located in client working directory
            log_level: str, optional
                level of logging. options are "debug", "info", "warning", "error", "critical"
                the default is "error".
        """
        return self.client.run_script_file(script_file_name, log_level)

    def upload_file(self, *file_list, show_progress=True):
        """Upload file(s) from the client to the server.

        Parameters
        ----------
            file_list: list of str
                list of paths to local file(s) that are to be uploaded
                wildcard characters "?" and "*" are supported
            show_progress: bool, optional
                whether showing the progress bar
                the default is True
        """
        self.client.upload_file(*file_list, show_progress=show_progress)

    def upload_file_from_example_repo(self, filename, dirname, show_progress=True):
        """Upload a file from Ansys example database to the server.

        Parameters
        ----------
            filename: str
                the file name
            dirname: str
                the subdirectory name under PyWorkbench folder
            show_progress: bool, optional
                whether showing the progress bar
                the default is True
        """
        self.client.upload_file_from_example_repo(filename, dirname, show_progress)

    def download_file(self, file_name, show_progress=True, target_dir=None):
        """Download file(s) from the server.

        Parameters
        ----------
            file_name: str
                the names of the files to be downloaded, located in the server's working directory
                wildcard characters "?" and "*" are supported
                when multiple files are being downloaded, a zip file will be created
            target_dir: str, optional
                the local directory for the downloaded files
                the default is the client working directory
            show_progress: bool, optional
                whether showing the progress bar
                the default is True
        """
        return self.client.download_file(
            file_name, show_progress=show_progress, target_dir=target_dir
        )

    def start_mechanical_server(self, system_name):
        """Start Mechanical server on the given system in Workbench project.

        Parameters
        ----------
            system_name: str
                the name of the system in Workbench project
        """
        return self.client.start_mechanical_server(system_name)

    def start_fluent_server(self, system_name):
        """Start Fluent server on the given system in Workbench project.

        Parameters
        ----------
            system_name: str
                the name of the system in Workbench project
        """
        return self.client.start_fluent_server(system_name)


"""Launch Workbench server on local or remote
Windows machine and create a Workbench client
that connects to the server. """


def launch_workbench(
    release="241", client_workdir=None, server_workdir=None, host=None, username=None, password=None
):
    """Launch Workbench on local or a remote computer

    Parameters
    ----------
    release: str, optional
        specific Workbench release to launch, such as "241"
    client_workdir: str, optional
        path to a writable working directory on the client computer
        the default is the system temp directory
    server_workdir: str, optional
        path to a writable working directory on the server computer
        the default is the WB user preference for temp project file folder
    host: str, optional
        server computer's name or IP. only for launching on a remote computer.
    username: str, optional
        login name on the server computer. only for launching on a remote computer.
    password: str, optional
        password on the server computer. only for launching on a remote computer.

    Returns
    -------
    an instance of PyWorkbench client that is connected to the launched server

    Examples
    --------
    Launch on the local computer
    >>> from ansys.workbench.core import launch_workbench
    >>> wb = launch_workbench()
    """
    return LaunchWorkbench(release, client_workdir, server_workdir, host, username, password)
