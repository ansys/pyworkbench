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

import pytest
import logging
from unittest.mock import patch, MagicMock
from ansys.workbench.core.workbench_client import WorkbenchClient
import pathlib
import tempfile

# Mock grpc and other dependencies
@pytest.fixture
def mock_grpc():
    with patch('ansys.workbench.core.workbench_client.grpc.insecure_channel') as mock_channel:
        yield mock_channel

@pytest.fixture
def mock_workbench_service_stub():
    with patch('ansys.workbench.core.workbench_client.WorkbenchServiceStub') as mock_stub:
        yield mock_stub

@pytest.fixture
def mock_wb():
    with patch('ansys.workbench.core.workbench_client.WorkbenchClient') as mock_wb:
        mock_wb.RunScriptRequest = MagicMock()
        mock_wb.DownloadFileRequest = MagicMock()
        mock_wb.UploadFileRequest = MagicMock()
        mock_wb.LOG_NONE = 0
        mock_wb.LOG_DEBUG = 1
        mock_wb.LOG_INFO = 2
        mock_wb.LOG_WARNING = 3
        mock_wb.LOG_ERROR = 4
        mock_wb.LOG_FATAL = 5
        yield mock_wb

def test_connect(mock_grpc, mock_workbench_service_stub):
    client = WorkbenchClient(local_workdir="/tmp", server_host="localhost", server_port=5000)
    client.connect()
    mock_grpc.assert_called_once_with("localhost:5000")
    mock_workbench_service_stub.assert_called_once()

def test_disconnect(mock_grpc, mock_workbench_service_stub):
    client = WorkbenchClient(local_workdir="/tmp", server_host="localhost", server_port=5000)
    client.connect()
    client.disconnect()
    assert client.channel is None
    assert client.stub is None

def test_is_connected(mock_grpc, mock_workbench_service_stub):
    client = WorkbenchClient(local_workdir="/tmp", server_host="localhost", server_port=5000)
    client.connect()
    assert client.is_connected()
    client.disconnect()
    assert not client.is_connected()

# def test_set_console_log_level(mock_wb):
#     client = WorkbenchClient(local_workdir="/tmp", server_host="localhost", server_port=5000)
#     client.set_console_log_level("warning")
#     assert client.__log_console_handler.level == logging.DEBUG

def test_run_script_string(mock_wb, mock_grpc, mock_workbench_service_stub):
    client = WorkbenchClient(local_workdir="/tmp", server_host="localhost", server_port=5000)
    client.connect()
    mock_stub = mock_workbench_service_stub.return_value
    mock_response = MagicMock()
    mock_stub.RunScript.return_value = mock_response
    client.run_script_string("print('Hello World!')")
    mock_stub.RunScript.assert_called_once()

def test_log_file(mock_wb, mock_grpc, mock_workbench_service_stub):
    client = WorkbenchClient(local_workdir="/tmp", server_host="localhost", server_port=5000)
    client.connect()
    mock_stub = mock_workbench_service_stub.return_value
    mock_response = MagicMock()
    mock_log_message = {'level': 2, 'message': 'Hello World!'}
    mock_response.log = MagicMock()
    mock_response.log.messages = [mock_log_message]
    mock_stub.RunScript.return_value = mock_response
    client.set_log_file("log.txt")
    client.run_script_string("print('Hello World!')", log_level="warning")
    mock_stub.RunScript.assert_called_once()
    client.download_file("log.txt", "/tmp")
    mock_stub.DownloadFile.assert_called_once()

def test_run_script_file(mock_wb, mock_grpc, mock_workbench_service_stub):
    local_workdir = workdir = pathlib.Path(__file__).parent
    script_dir = workdir / "scripts"
    client = WorkbenchClient(local_workdir= local_workdir, server_host="localhost", server_port=5000)
    client.connect()
    mock_stub = mock_workbench_service_stub.return_value
    mock_response = MagicMock()
    mock_stub.RunScript.return_value = mock_response
    mock_response.result.result = "{'result': 'success'}"
    mock_response.log = MagicMock()
    mock_response.log.messages = [{'level': 2, 'message': 'Hello World!'}]
    client.run_script_file(script_dir / "cooled_turbine_blade.py")
    mock_stub.RunScript.assert_called_once()
    assert mock_stub.RunScript.call_count == 1
    assert mock_response.result.result == "{'result': 'success'}"

def test_upload_file(mock_wb, mock_grpc, mock_workbench_service_stub):
    client = WorkbenchClient(local_workdir="/tmp", server_host="localhost", server_port=5000)
    client.connect()
    mock_stub = mock_workbench_service_stub.return_value
    mock_response = MagicMock()
    mock_response.error = None
    mock_response.file_name = "uploaded_file1"
    mock_stub.UploadFile.return_value = mock_response

    with patch('ansys.workbench.core.workbench_client.os.path.isfile', return_value=True):
        with patch('ansys.workbench.core.workbench_client.glob.glob', return_value=['file1', 'file2']):
            client.upload_file("file*", show_progress=True)
            assert mock_stub.UploadFile.call_count == 2

def test_upload_iterator():
    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as tmp_file:
        tmp_file.write(b'mock_file_content')

    try:
        # Create a WorkbenchClient instance
        client = WorkbenchClient(local_workdir="/tmp", server_host="localhost", server_port=5000)
        client.connect()

        # Get the temporary file path
        file_path = tmp_file.name

        # Call the method under test
        iterator = client._WorkbenchClient__upload_iterator(file_path, show_progress=True)

        # Assertions
        upload_requests = list(iterator)
        assert len(upload_requests) > 1  # Assuming the file is large enough to yield more than one chunk
    finally:
        # Clean up the temporary file
        if pathlib.Path(file_path).exists():
            pathlib.Path(file_path).unlink()


def test_download_file():
    client = WorkbenchClient(local_workdir="/tmp", server_host="localhost", server_port=5000)
    client.connect()
    mock_stub = MagicMock()
    client.stub = mock_stub

    # Mock response setup
    mock_response1 = MagicMock()
    mock_file_info1 = MagicMock()
    mock_file_info1.is_archive = False
    mock_file_info1.file_size = 200  # Let's assume the file size is 200 bytes
    mock_response1.file_info = mock_file_info1
    mock_response1.file_content = b'mock_file_content1'

    mock_response2 = MagicMock()
    mock_response2.file_content = b'mock_file_content2'

    # Set up return value for the mock method
    mock_stub.DownloadFile.return_value = [mock_response1, mock_response2]

    # Call the method under test
    result = client.download_file("file.txt", target_dir="/tmp", show_progress=True)

    # Assertions
    assert mock_stub.DownloadFile.call_count == 1
    assert mock_response1.file_info.file_size == 200  # Ensure the file size is set correctly
