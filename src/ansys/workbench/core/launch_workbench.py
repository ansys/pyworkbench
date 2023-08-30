import os
import logging
import tempfile
import time
import uuid
import wmi
from ansys.workbench.core.workbench_client import WorkbenchClient

class LaunchWorkbench:
    """launch Workbench server on local or remote Windows machine and create a Workbench client that connects to the server. """

    def __init__(self, release = '241', client_workdir = None, server_workdir = None, host = None, username = None, password = None):
        self._release = release
        self._server_workdir = server_workdir
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
        port = self._launch_server()
        if port is not None and port > 0:
            if host is None:
                host = 'localhost'
            self.client = WorkbenchClient(local_workdir = client_workdir, server_host = host, server_port = port)
            self.client.connect()

    def _launch_server(self):
        try:
            if self._host is None:
                self._wmi_connection = wmi.WMI()
            else:
                self._wmi_connection = wmi.WMI(self._host, user=self._username, password=self._password)
            logging.info("host connection established")

            install_path = None
            for ev in self._wmi_connection.Win32_Environment():
                if ev.Name == "AWP_ROOT" + self._release:
                    install_path = ev.VariableValue
                    break
            if install_path is None:
                install_path = "C:/Program Files/Ansys Inc/v" + self._release
                logging.warning("ANSYS installation not found. Assume the default location: " + install_path)
            else:
                logging.info("ANSYS installation found at: " + install_path)
            exePath = os.path.join(install_path, "Framework", "bin", "Win64", "RunWB2.exe")
            prefix = uuid.uuid4().hex
            workdir_arg = ''
            if self._server_workdir is not None:
                workdir_arg = ",WorkingDirectory=\'" + self._server_workdir + "\'"
            cmdLine = exePath + " -I -E \"StartServer(EnvironmentPrefix=\'" + prefix + "\'" + workdir_arg + ")\""
            
            process_startup_info = self._wmi_connection.Win32_ProcessStartup.new(ShowWindow=1)
            process_id, result = self._wmi_connection.Win32_Process.Create(
                CommandLine = cmdLine,
                ProcessStartupInformation = process_startup_info)

            if result == 0:
                logging.info("Workbench launched on the host with process id " + str(process_id))
                self._process_id = process_id
            else:
                logging.error("Workbench failed to launch on the host")
                return 0

            # retrieve server port once WB is fully up running
            port = None
            timeout = 60*8   # set 8 minutes as upper limit for WB startup
            start_time = time.time()
            while True:
                for ev in self._wmi_connection.Win32_Environment():
                    if ev.Name == "ANSYS_FRAMEWORK_SERVER_PORT":
                        port = ev.VariableValue
                        if port.startswith(prefix):
                            port = port[len(prefix):]
                            break
                        else:
                            port = None
                        break
                if port is not None:
                    break
                if time.time() - start_time > timeout:
                    logging.error("Failed to start Workbench service within reasonable timeout")
                    break;
                time.sleep(10)
            if port is None:
                logging.error("Failed to retrieve the port used by Workbench service")
            else:
                logging.info("Workbench service uses port " + port)

            return int(port)

        except wmi.x_wmi:
            logging.error("wrong credential")

    def exit(self):
        if self.client is not None:
            self.client.disconnect()
            self.client = None

        if self._wmi_connection is None:
            return

        # collect parent-children mapping
        children = { self._process_id : [] }
        process_by_id = {}
        for p in self._wmi_connection.Win32_Process():
            process_by_id[p.ProcessId] = p
            children.setdefault(p.ProcessId, [])
            if p.ParentProcessId is None:
                continue;
            children.setdefault(p.ParentProcessId, [])
            children[p.ParentProcessId].append(p.ProcessId)

        # terminate related processes bottom-up
        toTerminate = []
        thisLevel = set([ self._process_id ])
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
        self.client.set_console_log_level(log_level)

    def set_log_file(self, log_file):
        self.client.set_log_file(log_file)

    def reset_log_file(self):
        self.client.reset_log_file()

    def run_script_string(self, script_string, log_level='error'):
        return self.client.run_script_string(script_string, log_level)

    def run_script_file(self, script_file_name, log_level='error'):
        return self.client.run_script_file(script_file_name, log_level)

    def upload_file(self, *file_list, show_progress=True):
        self.client.upload_file(*file_list, show_progress=show_progress)

    def upload_file_from_example_repo(self, filename, dirname, show_progress=True):
        self.client.upload_file_from_example_repo(filename, dirname, show_progress)

    def download_file(self, file_name, show_progress=True, target_dir=None):
        return self.client.download_file(file_name, show_progress=show_progress, target_dir=target_dir)

    def start_pymechanical(self, system_name):
        return self.client.start_pymechanical(system_name)

    def start_pyfluent(self, system_name):
        return self.client.start_pyfluent(system_name)

"""launch Workbench server on local or remote Windows machine and create a Workbench client that connects to the server. """
def launch_workbench(
    release = '241',
    client_workdir = None,
    server_workdir = None,
    host = None,
    username = None,
    password = None):
    return LaunchWorkbench(release, client_workdir, server_workdir, host, username, password)