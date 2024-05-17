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


class ClientWrapper:
    def __init__(self, port, client_workdir=None, host=None):
        if host is None:
            host = "localhost"
        if client_workdir is None:
            client_workdir = tempfile.gettempdir()
        self._client = WorkbenchClient(
            local_workdir=client_workdir, server_host=host, server_port=port
        )
        self._client.connect()

    def set_console_log_level(self, log_level):
        """Set log filter level for the client console.

        Parameters
        ----------
        log_level : str
            level of logging: options are "debug", "info", "warning", "error", "critical"
            (default: "error")
        """
        self._client.set_console_log_level(log_level)

    def set_log_file(self, log_file):
        """Set a local log file for Workbench server log which overwrites previously
        set log file if any.

        Parameters
        ----------
        log_file : str
            path to a local file used for logging
        """
        self._client.set_log_file(log_file)

    def reset_log_file(self):
        """No longer use the current log file for Workbench server log."""
        self._client.reset_log_file()

    def run_script_string(self, script_string, log_level="error"):
        r"""Run the given script on the server.

        Parameters
        ----------
        script_string : str
            a string containing the content of the script to run
        log_level : str, optional
            level of logging: options are "debug", "info", "warning", "error", "critical"
            (default: "error")

        Returns
        -------
        str
            the output defined in the script.

        Examples
        --------
        Run a Workbench script, given in a string, that returns the name of
        a newly created system.

        >>> wb.run_script_string(r'''import json
        wb_script_result=json.dumps(GetTemplate(TemplateName="FLUENT").CreateSystem().Name)
        ''')

        """
        return self._client.run_script_string(script_string, log_level)

    def run_script_file(self, script_file_name, log_level="error"):
        """Run the given script file on the server.

        Parameters
        ----------
        script_file_name : str
            file name of the script, located in the client working directory
        log_level : str, optional
            level of logging: options are "debug", "info", "warning", "error", "critical"
            (default: "error")

        Returns
        -------
        str
            the output defined in the script.
        """
        return self._client.run_script_file(script_file_name, log_level)

    def upload_file(self, *file_list, show_progress=True):
        """Upload file(s) from the client to the server.

        Parameters
        ----------
        file_list : list[str]
            list of paths to the local file(s) that are to be uploaded, supporting
            wildcard characters "?" and "*"
        show_progress : bool, optional
            whether a progress bar should be shown during upload process
            (default: True)

        Returns
        -------
        list[str]
            the uploaded file names.
        """
        self._client.upload_file(*file_list, show_progress=show_progress)

    def upload_file_from_example_repo(self, filename, dirname, show_progress=True):
        """Upload a file from Ansys example database to the server.

        Parameters
        ----------
        filename : str
            the file name
        dirname : str
            the subdirectory name on the database under PyWorkbench folder
        show_progress : bool, optional
            whether a progress bar should be shown during upload process
            (default: True)
        """
        self._client.upload_file_from_example_repo(filename, dirname, show_progress)

    def download_file(self, file_name, show_progress=True, target_dir=None):
        """Download file(s) from the server.

        Parameters
        ----------
        file_name : str
            The name of the file to be downloaded, located in the server's working directory,
            supporting wildcard characters "?" and "*"; a zip file will be automatically
            generated/downloaded when multiple files are specified
        target_dir : str, optional
            Path to a local directory to put the downloaded files
            (default: the client working directory)
        show_progress : bool, optional
            Whether a progress bar should be shown during download process
            (default: True)

        Returns
        -------
        str
            The downloaded file name.
        """
        return self._client.download_file(
            file_name, show_progress=show_progress, target_dir=target_dir
        )

    def start_mechanical_server(self, system_name):
        """Start PyMechanical server for the given system in the Workbench project.

        Parameters
        ----------
        system_name : str
            The name of the system in the Workbench project.

        Returns
        -------
        int
            The port number used by the PyMechanical server which can be
            used to start a PyMechanical client.

        Examples
        --------
        Start PyMechanical session for the given system name.

        >>> from ansys.mechanical.core import launch_mechanical
        >>> server_port=wb.start_mechanical_server(system_name=mech_system_name)
        >>> mechanical = launch_mechanical(start_instance=False, port=server_port)

        """
        return self._client.start_mechanical_server(system_name)

    def start_fluent_server(self, system_name):
        """Start PyFluent server for the given system in the Workbench project.

        Parameters
        ----------
        system_name : str
            the name of the system in the Workbench project

        Returns
        -------
        str
            the path to a local file containing the PyFluent server info, which
            can be used to start a PyFluent client.

        Examples
        --------
        Start PyFluent session for the given system name.

        >>> import ansys.fluent.core as pyfluent
        >>> server_info_file=wb.start_fluent_server(system_name=fluent_sys_name)
        >>> fluent=pyfluent.connect_to_fluent(server_info_filepath=server_info_file)

        """
        return self._client.start_fluent_server(system_name)

    def start_sherlock_server(self, system_name):
        """Start PySherlock server for the given system in the Workbench project.

        Parameters
        ----------
        system_name : str
            The name of the system in the Workbench project.

        Returns
        -------
        int
            The port number used by the PySherlock server which can be
            used to start a PySherlock client.

        Examples
        --------
        Start PySherlock session for the given system name.

        >>> from ansys.sherlock.core import launcher
        >>> server_port=wb.start_sherlock_server(system_name=sherlock_system_name)
        >>> sherlock = launcher.launch_sherlock(port=server_port)
        >>> sherlock.common.check()

        """
        return self._client.start_sherlock_server(system_name)

    def exit(self):
        """Disconnect from the server."""
        if self._client is not None:
            self._client.disconnect()
            self._client = None


class LaunchWorkbench(ClientWrapper):
    def __init__(
        self,
        release="242",
        client_workdir=None,
        server_workdir=None,
        host=None,
        username=None,
        password=None,
    ):
        self._wmi_connection = None
        self._process_id = -1

        if len(release) != 3 or not release.isdigit():
            raise Exception("invalid ANSYS release number: " + release)
        port = self.__launch_server(host, release, server_workdir, username, password)
        if port is not None and port > 0:
            ClientWrapper.__init__(self, port, client_workdir, host)

    def __launch_server(self, host, release, server_workdir, username, password):
        try:
            if host is None:
                self._wmi_connection = wmi.WMI()
            else:
                if username is None or password is None:
                    raise Exception(
                        "username and passwork must be specified "
                        "to launch Workbench on a remote machine"
                    )
                self._wmi_connection = wmi.WMI(host, user=username, password=password)
            logging.info("host connection established")

            install_path = None
            for ev in self._wmi_connection.Win32_Environment():
                if ev.Name == "AWP_ROOT" + release:
                    install_path = ev.VariableValue
                    break
            if install_path is None:
                install_path = "C:/Program Files/Ansys Inc/v" + release
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
        ClientWrapper.exit(self)

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


class ConnectWorkbench(ClientWrapper):
    def __init__(
        self,
        port,
        client_workdir=None,
        host=None,
    ):
        ClientWrapper.__init__(self, port, client_workdir, host)


def launch_workbench(
    release="242", client_workdir=None, server_workdir=None, host=None, username=None, password=None
):
    """Launch PyWorkbench server on local or remote Windows machine and create
       a PyWorkbench client that connects to the server.

    Parameters
    ----------
    release : str, optional
        specify a Workbench release to launch (default: "242")
    client_workdir : str, optional
        path to a writable directory on the client computer
        (default: the system temp directory)
    server_workdir : str, optional
        path to a writable directory on the server computer
        (default: the user preference for Workbench temporary file folder)
    host : str, optional
        the server computer's name or IP address (default: None for launching on the local computer)
    username : str, optional
        user's login name on the server computer (default: None for launching on the local computer)
    password : str, optional
        user's password on the server computer (default: None for launching on the local computer)

    Returns
    -------
    LaunchWorkbench
        An instance of PyWorkbench client that is connected to the launched server.

    Examples
    --------
    Launch a server on the local computer and variable "wb" holds the returned client.

    >>> from ansys.workbench.core import launch_workbench
    >>> wb = launch_workbench()

    """
    return LaunchWorkbench(release, client_workdir, server_workdir, host, username, password)


def connect_workbench(port, client_workdir=None, host=None):
    """create a PyWorkbench client that connects to a already running PyWorkbench server.

    Parameters
    ----------
    port : int
        the port used by the server
    client_workdir : str, optional
        path to a writable directory on the client computer
        (default: the system temp directory)
    host : str, optional
        the server computer's name or IP address (default: None for the local computer)

    Returns
    -------
    ConnectWorkbench
        An instance of PyWorkbench client that is connected to the server.

    Examples
    --------
    connect to a server at port 32588 on localhost and variable "wb" holds the returned client.

    >>> from ansys.workbench.core import connect_workbench
    >>> wb = connect_workbench(port = 32588)

    """
    return ConnectWorkbench(port, client_workdir, host)


__all__ = ["launch_workbench", "connect_workbench"]
