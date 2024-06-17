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

"""Workbench client module for PyWorkbench."""

import glob
import json
import logging
import logging.handlers
from logging.handlers import WatchedFileHandler
import os

import grpc
import tqdm

from ansys.api.workbench.v0 import workbench_pb2 as wb
from ansys.api.workbench.v0.workbench_pb2_grpc import WorkbenchServiceStub
from ansys.workbench.core.example_data import ExampleData


class WorkbenchClient:
    """Functions of a PyWorkbench client.

    Parameters
    ----------
    local_workdir : str
        Local working directory for the client.
    server_host : str
        Hostname or IP address of the server.
    server_port : int
        Port number of the server.
    """

    def __init__(self, local_workdir, server_host, server_port):
        """Create a Workbench client."""
        self.workdir = local_workdir
        self._server_host = server_host
        self._server_port = server_port
        self.__init_logging()

    def __enter__(self):
        """Connect to the server when entering a context."""
        self._connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Disconnect from the server when exiting a context."""
        self._disconnect()

    def _connect(self):
        """Connect to the server."""
        hnp = self._server_host + ":" + str(self._server_port)
        self.channel = grpc.insecure_channel(hnp)
        self.stub = WorkbenchServiceStub(self.channel)
        logging.info("connected to the WB server at " + hnp)

    def _disconnect(self):
        """Disconnect from the server."""
        if self.channel:
            self.channel.close()
            self.channel = None
            self.stub = None
            logging.info("Disconnected from the Workbench server")

    def _is_connected(self):
        """Return whether this client is connected to the server."""
        return self.channel is not None

    def __init_logging(self):
        """Initialize logging for the client."""
        self._logger = logging.getLogger("WB")
        self._logger.setLevel(logging.DEBUG)
        self._logger.propagate = False
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        stream_handler.setLevel(logging.WARNING)
        self._logger.addHandler(stream_handler)
        self.__log_console_handler = stream_handler

    def set_console_log_level(self, log_level):
        """Set the log filter level for the client console.

        Parameters
        ----------
        log_level : str, default: "error"
            Level of logging. Options are "critical" "debug", "error", "info", and "warning".
        """
        self.__log_console_handler.setLevel(WorkbenchClient.__to_python_log_level(log_level))

    def set_log_file(self, log_file):
        """Set a local log file for the Workbench server log.

        Create a local log file if one does not exist and append it to the existing log file.

        Parameters
        ----------
        log_file : str
            Path to a local file to use for logging.
        """
        self.reset_log_file()

        file_handler = WatchedFileHandler(log_file)
        file_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        file_handler.setLevel(logging.DEBUG)
        self._logger.addHandler(file_handler)
        self.__log_file_handler = file_handler

    def reset_log_file(self):
        """No longer use the current log file for the Workbench server log."""
        if self.__log_file_handler is None:
            return
        self.__log_file_handler.close()
        self._logger.removeHandler(self.__log_file_handler)
        self.__log_file_handler = None

    __log_file_handler = None
    __log_console_handler = None

    def run_script_string(self, script_string, log_level="error"):
        """Run a script as given in the input string on the server.

        Parameters
        ----------
        script_string : str
            String containing the content of the script to run.
        log_level : str, default: "error"
            Level of logging. Options are "critical" "debug", "error", "info", and "warning".

        Returns
        -------
        str
            Output defined in the script.

        Examples
        --------
        Run a Workbench script, given in a string, that returns the name of
        a newly created system.

        >>> wb.run_script_string(r'''import json
        wb_script_result=json.dumps(GetTemplate(TemplateName="FLUENT").CreateSystem().Name)
        ''')

        """
        if not self._is_connected():
            logging.error("Workbench client is not yet connected to a server.")
        request = wb.RunScriptRequest(
            content=script_string, log_level=WorkbenchClient.__to_server_log_level(log_level)
        )
        for response in self.stub.RunScript(request):
            if response.log and response.log.messages and len(response.log.messages) > 0:
                for log_entry in response.log.messages:
                    self.__python_logging(log_entry.level, log_entry.message)
            if response.result:
                if response.result.error:
                    logging.error("Error when running the script: " + response.result.error)
                    return None
                elif response.result.result:
                    logging.info("The script has finisished.")
                    return json.loads(response.result.result)

    def run_script_file(self, script_file_name, log_level="error"):
        """Run a script file on the server.

        Parameters
        ----------
        script_file_name : str
            Name of the script file to run. The script file should be located in the client
            working directory
        log_level : str, default: "error"
            Level of logging. Options are "critical" "debug", "error", "info", and "warning".

        Returns
        -------
        str
            Output defined in the script.
        """
        if not self._is_connected():
            logging.error("Workbench client is not yet connected to a server")
        script_path = os.path.join(self.workdir, script_file_name)
        with open(script_path, encoding="utf-8-sig") as sf:
            script_string = sf.read()
        return self.run_script_string(script_string, log_level)

    def upload_file(self, *file_list, show_progress=True):
        """Upload one or more files from the client to the server.

        Parameters
        ----------
        file_list : list[str]
            List of paths to the one or more local files to upload. The
            wildcard characters "?" and "*" are supported.
        show_progress : bool, default: True
            Whether to show a progress bar during the upload.

        Returns
        -------
        list[str]
            Names of the uploaded files.
        """
        if not self._is_connected():
            logging.error("Workbench client is not yet connected to a server.")
        requested = []
        for file_pattern in file_list:
            if "*" in file_pattern or "?" in file_pattern:
                if not os.path.isabs(file_pattern):
                    file_pattern = os.path.join(self.workdir, file_pattern)
                requested.extend(glob.glob(file_pattern))
            else:
                requested.append(file_pattern)
        existing_files = []
        nonexisting_files = []
        for file_name in requested:
            if not os.path.isabs(file_name):
                file_name = os.path.join(self.workdir, file_name)
            if os.path.isfile(file_name):
                existing_files.append(file_name)
            else:
                nonexisting_files.append(file_name)
        if len(nonexisting_files) > 0:
            logging.warning(
                "The following files do not exist and are skipped: " + "\n".join(nonexisting_files)
            )
        for file_path in existing_files:
            logging.info(f"uploading file {file_path}")
            response = self.stub.UploadFile(self.__upload_iterator(file_path, show_progress))
            if response.error:
                logging.error("Error during file upload: " + response.error)
            else:
                logging.info(
                    "A file is uploaded to the server with the name: " + response.file_name
                )

    def __upload_iterator(self, file_path, show_progress):
        dir_path, file_name = os.path.split(file_path)
        yield wb.UploadFileRequest(file_name=file_name)

        pbar = None
        if show_progress:
            bytes = os.path.getsize(file_path)
            pbar = tqdm.tqdm(
                total=bytes,
                desc=f"Uploading {file_name}",
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
            )

        chunk_size = 65536  ## 64 kb
        with open(file_path, mode="rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if chunk:
                    if pbar is not None:
                        pbar.update(len(chunk))
                    yield wb.UploadFileRequest(file_content=chunk)
                else:
                    if pbar is not None:
                        pbar.close()
                    return

    def upload_file_from_example_repo(self, relative_file_path, show_progress=True):
        """Upload a file from the Ansys ``example-data`` repository to the server.

        Parameters
        ----------
        relative_file_path : str
            File path relative to the ``pyworkbench`` folder in the ``example-data`` repository.
        show_progress : bool, default: True
            Whether to show a progress bar during the upload.
        """
        if not self._is_connected():
            logging.error("Workbench client is not yet connected to a server.")
        downloaded = ExampleData.download(relative_file_path, self.workdir)
        self.upload_file(downloaded, show_progress=show_progress)

    def download_file(self, file_name, show_progress=True, target_dir=None):
        """Download one or more files from the server.

        Parameters
        ----------
        file_name : str
            Name of the file. File must be located in the server's working directory.
            The wildcard characters "?" and "*" are supported. A ZIP file is automatically
            generated and downloaded when multiple files are specified.
        show_progress : bool, default: True
            Whether to show a progress bar during the download.
        target_dir : str, default: None
            Path to a local directory to download the files to. The default is ``None``,
            in which case the client working directory is used.


        Returns
        -------
        str
            Name of the downloaded file.
        """
        if not self._is_connected():
            logging.error("Workbench client is not yet connected to a server.")
        request = wb.DownloadFileRequest(file_name=file_name)
        file_name = file_name.replace("*", "_").replace("?", "_")
        td = target_dir
        if td is None:
            td = self.workdir
        file_path = os.path.join(td, file_name)
        pbar = None
        started = False
        for response in self.stub.DownloadFile(request):
            if response.error:
                logging.error("Error during file download: " + response.error)
                return None
            if response.file_info:
                if response.file_info.is_archive:
                    file_name += ".zip"
                    file_path += ".zip"
                if response.file_info.file_size > 0:
                    if show_progress:
                        pbar = tqdm.tqdm(
                            total=response.file_info.file_size,
                            desc=f"Downloading {file_name}",
                            unit="B",
                            unit_scale=True,
                            unit_divisor=1024,
                        )
            if response.file_content:
                size = len(response.file_content)
                if size > 0:
                    if not started:
                        if os.path.exists(file_path):
                            os.remove(file_path)
                        started = True
                    with open(file_path, mode="ab") as f:
                        f.write(response.file_content)
                    if pbar is not None:
                        pbar.update(size)
        logging.info(f"Dwnloaded the file {file_name}.")
        if pbar is not None:
            pbar.close()
        return file_name

    def __python_logging(self, log_level, msg):
        """Log a message with the given log level.

        Parameters
        ----------
        log_level : int
            log level. Options are ``logging.CRITICAL``, ``logging.DEBUG``, ``logging.ERROR``,
            ``logging.INFO``, and ``logging.WARNING``.

        msg : str
            Message to log.
        """
        if log_level == wb.LOG_DEBUG:
            self._logger.debug(msg)
        elif log_level == wb.LOG_INFO:
            self._logger.info(msg)
        elif log_level == wb.LOG_WARNING:
            self._logger.warn(msg)
        elif log_level == wb.LOG_ERROR:
            self._logger.error(msg)
        elif log_level == wb.LOG_FATAL:
            self._logger.fatal(msg)

    @staticmethod
    def __to_python_log_level(log_level):
        """Convert the given log level to the corresponding Python log level.

        Parameters
        ----------
        log_level : str
            level of logging: options are "debug", "info", "warning", "error", "critical"

        Returns
        -------
        int
            the corresponding Python log level
        """
        log_level = log_level.lower()
        for level_name, server_level in WorkbenchClient.__log_levels.items():
            if log_level in level_name:
                return server_level[1]
        return logging.NOTSET

    @staticmethod
    def __to_server_log_level(log_level):
        """Convert the given log level to the corresponding server log level.

        Parameters
        ----------
        log_level : str
            Level of logging. Options are "critical" "debug", "error", "info", and "warning".

        Returns
        -------
        int
            Corresponding server log level.
        """
        log_level = log_level.lower()
        for level_name, server_level in WorkbenchClient.__log_levels.items():
            if log_level in level_name:
                return server_level[0]
        return wb.LOG_NONE

    __log_levels = {
        "none null": (wb.LOG_NONE, logging.NOTSET),
        "debug": (wb.LOG_DEBUG, logging.DEBUG),
        "information": (wb.LOG_INFO, logging.INFO),
        "warning": (wb.LOG_WARNING, logging.WARNING),
        "error": (wb.LOG_ERROR, logging.ERROR),
        "fatal critical": (wb.LOG_FATAL, logging.CRITICAL),
    }

    def start_mechanical_server(self, system_name):
        """Start the PyMechanical server for the given system in the Workbench project.

        Parameters
        ----------
        system_name : str
            Name of the system in the Workbench project.

        Returns
        -------
        int
            Port of the PyMechanical server to use to start the PyMechanical client.

        Examples
        --------
        Start a PyMechanical session for the given system name.

        >>> from ansys.mechanical.core import launch_mechanical
        >>> server_port=wb.start_mechanical_server(system_name=mech_system_name)
        >>> mechanical = launch_mechanical(start_instance=False, port=server_port)

        """
        pymech_port = self.run_script_string(
            f"""import json
server_port=LaunchMechanicalServerOnSystem(SystemName="{system_name}")
wb_script_result=json.dumps(server_port)
"""
        )
        return pymech_port

    def start_fluent_server(self, system_name):
        """Start the PyFluent server for the given system in the Workbench project.

        Parameters
        ----------
        system_name : str
            Name of the system in the Workbench project.

        Returns
        -------
        str
            Path to the local file containing the PyFluent server information that
            can be used to start a PyFluent client.

        Examples
        --------
        Start a PyFluent session for the given system name.

        >>> import ansys.fluent.core as pyfluent
        >>> server_info_file=wb.start_fluent_server(system_name=fluent_sys_name)
        >>> fluent=pyfluent.connect_to_fluent(server_info_file_name=server_info_file)

        """
        server_info_file_name = self.run_script_string(
            f"""import json
server_info_file=LaunchFluentServerOnSystem(SystemName="{system_name}")
wb_script_result=json.dumps(server_info_file)
"""
        )
        local_copy = os.path.join(self.workdir, server_info_file_name)
        if os.path.exists(local_copy):
            os.remove(local_copy)
        self.download_file(server_info_file_name, show_progress=False)
        return local_copy

    def start_sherlock_server(self, system_name):
        """Start the PySherlock server for the given system in the Workbench project.

        Parameters
        ----------
        system_name : str
            Name of the system in the Workbench project.

        Returns
        -------
        int
            Port of the PySherlock server to use to start a PySherlock client.

        Examples
        --------
        Start a PySherlock session for the given system name.

        >>> from ansys.sherlock.core import pysherlock
        >>> server_port=wb.start_sherlock_server(system_name=sherlock_system_name)
        >>> sherlock = pysherlock.connect_grpc_channel(port=server_port)
        >>> sherlock.common.check()

        """
        pysherlock_port = self.run_script_string(
            f"""import json
server_port=LaunchSherlockServerOnSystem(SystemName="{system_name}")
wb_script_result=json.dumps(server_port)
"""
        )
        return pysherlock_port


__all__ = ["WorkbenchClient"]
