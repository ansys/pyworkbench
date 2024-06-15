# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
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

"""Module for starting PyWorkbench."""

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


class ClientWrapper(WorkbenchClient):
    """Provides for connecting to a Workbench server.

    Parameters
    ----------
    port : int
        Port used by the server.
    client_workdir : str, default: None
        Path to a writable directory on the client computer.
    host : str, default: None
        Server computer's name or IP address.
    """

    def __init__(self, port, client_workdir=None, host=None):
        """Create a PyWorkbench client that connects to a Workbench server."""
        if host is None:
            host = "localhost"
        if client_workdir is None:
            client_workdir = tempfile.gettempdir()
        super().__init__(client_workdir, host, port)
        super()._connect()

    def exit(self):
        """Disconnect from the server."""
        if super()._is_connected():
            super()._disconnect()


class LaunchWorkbench(ClientWrapper):
    """Launch a Workbench server on a local or remote Windows machine.

    Parameters
    ----------
    release : str, default: "242"
        Workbench release to launch.
    client_workdir : str, default: None
        Path to a writable directory on the client computer. The default is ``None``,
        in which case the system temp directory is used.
    server_workdir : str, None
        Path to a writable directory on the server computer. The default is ``None``,
        in which case the user preference for the Workbench temporary file folder is used.
    host : str, None
        Server computer's name or IP address. The default is ``None`` for launching on the
        local computer.
    username : str, None
        User's login name on the server computer. The default is ``None`` for launching on
        the local computer.
    password : str, None
        User's password on the server computer. The default is ``None`` for launching on
        the local computer.

    Raises
    ------
    Exception
        If the Ansys release number is invalid.

    Examples
    --------
    Launch a server on the local computer and use the ``wb`` variable to hold the returned client.

    >>> from ansys.workbench.core import launch_workbench
    >>> wb = launch_workbench()
    """

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

        if (
            len(release) != 3
            or not release.isdigit()
            or release[0] not in ["2", "3"]
            or release[2] not in ["1", "2"]
        ):
            raise Exception("Invalid ANSYS release: " + release)
        port = self.__launch_server(host, release, server_workdir, username, password)
        if port is None or port <= 0:
            raise Exception("Filed to launch Ansys Workbench service.")
        super().__init__(port, client_workdir, host)

    def __launch_server(self, host, release, server_workdir, username, password):
        """Launch a Workbench server on the local or a remote Windows machine."""
        try:
            if host is None:
                self._wmi_connection = wmi.WMI()
            else:
                if username is None or password is None:
                    raise Exception(
                        "Username and passwork must be specified "
                        "to launch Workbench on a remote machine."
                    )
                self._wmi_connection = wmi.WMI(host, user=username, password=password)
            logging.info("Host connection is established.")

            install_path = None
            for ev in self._wmi_connection.Win32_Environment():
                if ev.Name == "AWP_ROOT" + release:
                    install_path = ev.VariableValue
                    break
            if install_path is None:
                install_path = "C:/Program Files/Ansys Inc/v" + release
                logging.warning(
                    "Ansys installation is not found. Assume the default location: " + install_path
                )
            else:
                logging.info("Ansys installation is found at: " + install_path)
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
                logging.error("Workbench failed to launch on the host.")
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
                    logging.error("Failed to start Workbench service within reasonable timeout.")
                    break
                time.sleep(10)
            if port is None:
                logging.error("Failed to retrieve the port used by Workbench service.")
            else:
                logging.info("Workbench service uses port " + port)

            return int(port)

        except wmi.x_wmi:
            logging.error("wrong credential")

    def exit(self):
        """Terminate the Workbench server and disconnect the client."""
        super().exit()

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
        to_terminate = []
        this_level = set([self._process_id])
        while True:
            next_level = set()
            for p in this_level:
                next_level.update(children[p])
            if len(next_level) == 0:
                break
            to_terminate.append(next_level)
            this_level = next_level
        for ps in reversed(to_terminate):
            for p in ps:
                logging.info("Shutting down " + process_by_id[p].Name + " ...")
                try:
                    process_by_id[p].Terminate()
                except Exception:
                    pass

        logging.info("Workbench server connection has ended.")
        self._wmi_connection = None
        self._process_id = -1


def launch_workbench(
    release="242", client_workdir=None, server_workdir=None, host=None, username=None, password=None
):
    """Launch PyWorkbench server on the local or a remote Windows machine.

    This method launch a Workbench server on the local or a remote Windows machine and creates
    a PyWorkbench client that connects to the server.

    Parameters
    ----------
    release : str, default: "251"
        Workbench release to launch.
    client_workdir : str, default: None
        Path to a writable directory on the client computer. The default is ``None``,
        in which case the system temp directory is used.
    server_workdir : str, None
        Path to a writable directory on the server computer. The default is ``None``,
        in which case the user preference for the Workbench temporary file folder is used.
    host : str, None
        Server computer's name or IP address. The default is ``None`` for launching on the
        local computer.
    username : str, None
        User's login name on the server computer. The default is ``None`` for launching on
        the local computer.
    password : str, None
        User's password on the server computer. The default is ``None`` for launching on
        the local computer.

    Returns
    -------
    WorkbenchClient
        Instance of the PyWorkbench client that is connected to the launched server.

    Examples
    --------
    Launch a server on the local computer and use the ``wb`` variable to hold the returned client.

    >>> from ansys.workbench.core import launch_workbench
    >>> wb = launch_workbench()

    """
    return LaunchWorkbench(release, client_workdir, server_workdir, host, username, password)


def connect_workbench(port, client_workdir=None, host=None):
    """Create a PyWorkbench client that connects to an already running Workbench server.

    Parameters
    ----------
    port : int
        Port used by the server.
    client_workdir : str, default: None
        Path to a writable directory on the client computer. The default is ``None``,
        in which case the system temp directory is used.
    host : str, default: None
        Server computer's name or IP address. The default is ``None`` for the local computer.

    Returns
    -------
    WorkbenchClient
        Instance of the PyWorkbench client that is connected to the server.

    Examples
    --------
    Connect to a server at port 32588 on localhost and use the ``wb`` variable to hold the
    returned client.

    >>> from ansys.workbench.core import connect_workbench
    >>> wb = connect_workbench(port = 32588)
    """
    return ClientWrapper(port, client_workdir, host)


__all__ = ["launch_workbench", "connect_workbench"]
