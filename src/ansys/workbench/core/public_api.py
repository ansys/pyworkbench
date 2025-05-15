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

"""Module for public API on PyWorkbench."""

import logging
import tempfile

from ansys.workbench.core.workbench_client import WorkbenchClient
from ansys.workbench.core.workbench_launcher import Launcher


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
    """Launch a Workbench server on a local machine or a remote Windows machine.

    Parameters
    ----------
    show_gui : bool, default: True
        Weather to launch Workbench in UI mode.
    version : str, default: None
        Workbench version to launch. It must be a 3-digit version that is "242" or later.
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
        If PyWorkbench server failed to launch.

    Examples
    --------
    Launch a server on the local computer and use the ``wb`` variable to hold the returned client.

    >>> from ansys.workbench.core import launch_workbench
    >>> wb = launch_workbench()
    """

    def __init__(
        self,
        show_gui=True,
        version=None,
        client_workdir=None,
        server_workdir=None,
        host=None,
        username=None,
        password=None,
    ):
        if not version:
            version = "251"

        self._launcher = Launcher()
        port = self._launcher.launch(version, show_gui, server_workdir, host, username, password)
        if port is None or port <= 0:
            raise Exception("Filed to launch Ansys Workbench service.")
        super().__init__(port, client_workdir, host)

    def exit(self):
        """Terminate the Workbench server and disconnect the client."""
        self.run_script_string("Reset()")
        self.run_script_string("internal_wbexit()")

        super().exit()

        self._launcher.exit()
        logging.info("Workbench server connection has ended.")


def launch_workbench(
    show_gui=True,
    version=None,
    client_workdir=None,
    server_workdir=None,
    host=None,
    username=None,
    password=None,
):
    """Launch PyWorkbench server on the local machine or a remote Windows machine.

    This method launch a Workbench server on the local machine or a remote Windows machine
    and creates a PyWorkbench client that connects to the server.

    Parameters
    ----------
    show_gui : bool, default: True
        Weather to launch Workbench in UI mode.
    version : str, default: None
        Workbench version to launch. It must be a 3-digit version that is "242" or later.
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
    return LaunchWorkbench(
        show_gui, version, client_workdir, server_workdir, host, username, password
    )


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
