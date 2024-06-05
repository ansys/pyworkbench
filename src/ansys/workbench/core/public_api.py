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

"""Module provides a function to launch a Workbench server on a local or remote Windows machine."""

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
    def __init__(self, port, client_workdir=None, host=None):
        if host is None:
            host = "localhost"
        if client_workdir is None:
            client_workdir = tempfile.gettempdir()
        super().__init__(client_workdir, host, port)
        _connect()

    def exit(self):
        """Disconnect from the server."""
        if _is_connected():
            _disconnect()


class LaunchWorkbench(ClientWrapper):
    """Launch a Workbench server on a local or remote Windows machine.

    Parameters
    ----------
    release : str, optional
        specify a Workbench release to launch. default: "241"
    client_workdir : str, optional
        path to a writable directory on the client computer. default: None
    server_workdir : str, optional
        path to a writable directory on the server computer. default: None
    host : str, optional
        the server computer's name or IP address. default: None
    username : str, optional
        user's login name on the server computer. default: None
    password : str, optional
        user's password on the server computer. default: None

    Raises
    ------
    Exception
        If the ANSYS release number is invalid.

    Examples
    --------
    Launch a server on the local computer and variable "wb" holds the returned client.

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

        if len(release) != 3 or not release.isdigit() or
            not release[0] in ['2', '3'] or not release[2] in ['1', '2']:
            raise Exception("invalid ANSYS release: " + release)
        port = self.__launch_server(host, release, server_workdir, username, password)
        if port is None or port <= 0:
            raise Exception("failed to launch ANSYS Workbench service")
        super().__init__(port, client_workdir, host)

    def __launch_server(self, host, release, server_workdir, username, password):
        """Launch a Workbench server on the local or a remote Windows machine.
        """
        try:
            if self._host is None:
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
        toTerminate = []  # noqa: N806 # TODO: Variable `toTerminate` in function should be lowercase to_terminate
        thisLevel = set([self._process_id])  # noqa: N806 # TODO: Variable `thisLevel` in function should be lowercase ``this_level``
        while True:
            nextLevel = set()  # noqa: N806 # TODO: Variable `nextLevel` in function should be lowercase next_level
            for p in thisLevel:
                nextLevel.update(children[p])
            if len(nextLevel) == 0:
                break
            toTerminate.append(nextLevel)
            thisLevel = nextLevel  # noqa: N806 # TODO: Variable `thisLevel` in function should be lowercase this_level
        for ps in reversed(toTerminate):
            for p in ps:
                logging.info("shutting down " + process_by_id[p].Name + " ...")
                try:
                    process_by_id[p].Terminate()
                except Exception:
                    pass

        logging.info("Workbench server ended")
        self._wmi_connection = None
        self._process_id = -1


def launch_workbench(
    release="242", client_workdir=None, server_workdir=None, host=None, username=None, password=None
):
    """Launch PyWorkbench server on the local or a remote Windows machine.

    Launch a Workbench server on the local or a remote Windows machine and create
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
    ClientWrapper
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
    ClientWrapper
        An instance of PyWorkbench client that is connected to the server.

    Examples
    --------
    connect to a server at port 32588 on localhost and variable "wb" holds the returned client.

    >>> from ansys.workbench.core import connect_workbench
    >>> wb = connect_workbench(port = 32588)
    """
    return ClientWrapper(port, client_workdir, host)


__all__ = ["launch_workbench", "connect_workbench"]
