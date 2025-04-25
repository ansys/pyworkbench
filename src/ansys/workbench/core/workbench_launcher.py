# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Module for launching PyWorkbench."""

import ctypes
import logging
import os
import platform
import time
import uuid


class Launcher:
    """Launch a Workbench server on a local or remote machine.
       Remote Linux launching is not supported.

    Raises
    ------
    Exception
        If the Ansys version number is invalid.
    """

    def __init__(self):
        try:
            self._wmi = None
            if platform.system() == "Windows":
                import wmi

                self._wmi = wmi
        except ImportError:
            # 'wmi' cannot be imported
            self._wmi = None

        if not self._wmi:
            try:
                self._libc = ctypes.CDLL("libc.so.6")
            except:
                self._libc = None
            if not self._libc:
                raise Exception(
                    "Required Python module does not exist or not working properly: either WMI or ctypes.CDLL"
                )

        self._wmi_connection = None
        self._process_id = -1
        self._port = None

    def launch(
        self,
        version,
        show_gui=True,
        server_workdir=None,
        host=None,
        username=None,
        password=None,
    ):
        """Launch PyWorkbench server on the local or a remote computer.

        Parameters
        ----------
        version : str
            Workbench version to launch. It must be a 3-digit version that is "242" or later.
        show_gui : bool, default: True
            Weather to launch Workbench in UI mode.
        server_workdir : str, default: None
            Path to a writable directory on the server computer. The default is ``None``,
            in which case the user preference for the Workbench temporary file folder is used.
        host : str, default: None
            Server computer's name or IP address. The default is ``None`` for launching on the
            local computer.
        username : str, default: None
            User's login name on the server computer. The default is ``None`` for launching on
            the local computer.
        password : str, default: None
            User's password on the server computer. The default is ``None`` for launching on
            the local computer.

        Raises
        ------
        Exception
            If the Ansys version string is invalid.
            If wmi service is not available for remote launching
            If the host is given but username or password is missing.
        """

        if (
            not version
            or len(version) != 3
            or not version.isdigit()
            or version[0] not in ["2", "3"]
            or version[2] not in ["1", "2"]
        ):
            raise Exception("Invalid ANSYS version: " + version)

        if host and not self._wmi:
            raise Exception("Launching PyWorkbench on a remote machine from Linux is not supported")

        if host and (not username or not password):
            raise Exception(
                "Username and passwork must be specified "
                "to launch PyWorkbench on a remote machine."
            )

        if self._wmi:
            try:
                if not host:
                    self._wmi_connection = self._wmi.WMI()
                else:
                    self._wmi_connection = self._wmi.WMI(host, user=username, password=password)
                logging.info("Host connection is established.")
            except self._wmi.x_wmi:
                if host:
                    raise Exception(
                        "Launching PyWorkbench on a remote machine failed. "
                        "Make sure that the remote host is a Windows machine and that "
                        "correct credential is used."
                    )
                else:
                    raise Exception("Launching PyWorkbench failed.")

        ansys_install_path = self.__getenv("AWP_ROOT" + version)
        if ansys_install_path:
            logging.info("Ansys installation is found at: " + ansys_install_path)
        else:
            raise Exception("Ansys installation is not found.")

        args = []
        if platform.system() == "Windows":
            exe_loc = os.path.join("Win64", "RunWB2.exe")
        else:
            exe_loc = os.path.join("Linux64", "runwb2")
        executable = os.path.join(ansys_install_path, "Framework", "bin", exe_loc)
        args.append(executable)
        if show_gui:
            args.append("-I")
        else:
            args.append("--start-and-wait")
            args.append("-nowindow")
        args.append("-E")
        prefix = uuid.uuid4().hex
        cmd = "\"StartServer(EnvironmentPrefix='"
        cmd += prefix + "'"
        workdir_arg = ""
        if server_workdir is not None:
            # use forward slash only to avoid escaping as command line argument
            server_workdir = server_workdir.replace("\\", "/")
            cmd += ",WorkingDirectory='" + server_workdir + "'"
        cmd += ')"'
        args.append(cmd)
        command_line = " ".join(args)

        successful = False
        if self._wmi:
            process_startup_info = self._wmi_connection.Win32_ProcessStartup.new(ShowWindow=1)
            process_id, result = self._wmi_connection.Win32_Process.Create(
                CommandLine=command_line, ProcessStartupInformation=process_startup_info
            )
            if result == 0:
                successful = True
                self._process_id = process_id
                for p in self._wmi_connection.Win32_Process():
                    if p.ProcessId == process_id:
                        self._process = p
                        break
        else:
            process = subprocess.Popen(args)
            if process:
                successful = True
                self._process_id = process.pid
                self._process = process
        if successful:
            logging.info("Workbench launched on the host with process id: " + str(self._process_id))
        else:
            logging.error("Workbench failed to launch on the host.")
            return 0

        # retrieve server port once WB is fully up running
        port = None
        timeout = 60 * 8  # set 8 minutes as upper limit for WB startup
        start_time = time.time()
        while True:
            port = self.__getenv("ANSYS_FRAMEWORK_SERVER_PORT")
            if port and port.startswith(prefix):
                port = port[len(prefix) :]
                break
            else:
                port = None
            if time.time() - start_time > timeout:
                logging.error("Failed to start Workbench service within reasonable timeout.")
                break
            time.sleep(10)
        if not port or int(port) <= 0:
            logging.error("Failed to retrieve the port used by Workbench service.")
            return 0
        logging.info("Workbench service uses port " + port)
        return int(port)

    def __getenv(self, key):
        value = None
        if self._wmi:
            for ev in self._wmi_connection.Win32_Environment():
                if ev.Name == key:
                    value = ev.VariableValue
        elif self._libc:
            getenv = self._libc.getenv
            getenv.restype = ctypes.c_char_p
            value = getenv(key)
        else:
            raise Exception("unexpected code path")
        return value

    def exit(self):
        """Terminate the launched Workbench server."""
        if self._process:
            try:
                if self._wmi:
                    self._process.Terminate()
                else:
                    self._process.terminate()
            except:
                pass

        """
        # terminate related processes bottom-up
        if self._wmi_connection:
            for p in self.__collect_process_tree():
                logging.info("Shutting down " + p.Name + " ...")
                try:
                    p.Terminate()
                except Exception:
                    pass
        """
        self._wmi_connection = None
        self._process_id = -1
        self._process = None

    def __collect_process_tree(self):
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

        # collect related processes
        process_ids_parent_first = []
        this_level = set([self._process_id])
        while True:
            next_level = set()
            for p in this_level:
                next_level.update(children[p])
            if len(next_level) == 0:
                break
            process_ids_parent_first.append(next_level)
            this_level = next_level

        # return the processes child-first-order
        processes_child_first = []
        for pid in reversed(process_ids_parent_first):
            processes_child_first.append(process_by_id[pid])
        return processes_child_first
