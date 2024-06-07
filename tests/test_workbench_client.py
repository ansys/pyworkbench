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

"""Tests for workbench client."""

import pathlib
import tempfile
from unittest.mock import MagicMock, patch

import pytest

from ansys.workbench.core import connect_workbench
from ansys.workbench.core.workbench_client import WorkbenchClient


# Mock grpc and other dependencies
@pytest.fixture
def mock_grpc():
    """Mock the insecure_channel method."""
    with patch("ansys.workbench.core.workbench_client.grpc.insecure_channel") as mock_channel:
        yield mock_channel


@pytest.fixture
def mock_workbench_service_stub():
    """Mock the WorkbenchServiceStub class."""
    with patch("ansys.workbench.core.workbench_client.WorkbenchServiceStub") as mock_stub:
        yield mock_stub


@pytest.fixture
def mock_wb():
    """Mock the WorkbenchClient class."""
    with patch("ansys.workbench.core.workbench_client.WorkbenchClient") as mock_wb:
        mock_wb.RunScriptRequest = MagicMock()
        mock_wb.DownloadFileRequest = MagicMock()
        mock_wb.UploadFileRequest = MagicMock()
        mock_wb.run_script_string = MagicMock()
        yield mock_wb


def test_connect(mock_grpc, mock_workbench_service_stub):
    """Test the connect method."""
    client = WorkbenchClient(local_workdir="/tmp", server_host="localhost", server_port=5000)
    client._connect()
    mock_grpc.assert_called_once_with("localhost:5000")
    mock_workbench_service_stub.assert_called_once()


def test_connect_workbench():
    """Test the connect_workbench method."""
    client = connect_workbench(port=5000, client_workdir="/tmp", host="localhost")
    assert isinstance(client, WorkbenchClient)
    client.exit()


def test_disconnect():
    """Test the disconnect method."""
    client = WorkbenchClient(local_workdir="/tmp", server_host="localhost", server_port=5000)
    client._connect()
    client._disconnect()
    assert client.channel is None
    assert client.stub is None


def test_is_connected():
    """Test the is_connected method."""
    client = WorkbenchClient(local_workdir="/tmp", server_host="localhost", server_port=5000)
    client._connect()
    assert client._is_connected()
    client._disconnect()
    assert not client._is_connected()


# def test_set_console_log_level(mock_wb):
#     client = WorkbenchClient(local_workdir="/tmp", server_host="localhost", server_port=5000)
#     client.set_console_log_level("warning")
#     assert client.__log_console_handler.level == logging.DEBUG


def test_run_script_string(mock_workbench_service_stub):
    """Test the run_script_string method."""
    client = WorkbenchClient(local_workdir="/tmp", server_host="localhost", server_port=5000)
    client._connect()
    mock_stub = mock_workbench_service_stub.return_value
    mock_response = MagicMock()
    mock_stub.RunScript.return_value = mock_response
    client.run_script_string("print('Hello World!')")
    mock_stub.RunScript.assert_called_once()


def test_log_file(mock_wb, mock_workbench_service_stub):
    """Test the log file functionality."""
    client = WorkbenchClient(local_workdir="/tmp", server_host="localhost", server_port=5000)
    client._connect()
    mock_stub = mock_workbench_service_stub.return_value
    mock_response = MagicMock()
    mock_response.log.messages = [{"level": 2, "message": "Hello World!"}]
    mock_response.log = MagicMock()
    mock_response.result.result = '{"key": "value"}'  # Assuming a successful result
    client.set_log_file("mock_log_file.log")
    client.run_script_string("print('Hello World!')", log_level="warning")
    mock_stub.RunScript.assert_called_once()
    client.download_file("log.txt", "/tmp")
    mock_stub.DownloadFile.assert_called_once()
    client.run_script_string("print('Hello World!')", log_level=mock_wb.LOG_DEBUG)
    with patch.object(client.stub, "RunScript", return_value=[mock_response]):
        # Call the method under test
        client.run_script_string("print('Hello World!')", log_level="info")
        for log_entry in mock_response.log.messages:
            assert "level" in log_entry
            assert "message" in log_entry


class LogMessage:
    """A class to represent a log message."""

    def __init__(self, level, message):
        self.level = level
        self.message = message


def test_run_script_file(mock_workbench_service_stub):
    """Test the run_script_file method."""
    local_workdir = workdir = pathlib.Path(__file__).parent
    script_dir = workdir / "scripts"
    client = WorkbenchClient(local_workdir=local_workdir, server_host="localhost", server_port=5000)
    client._connect()
    mock_stub = mock_workbench_service_stub.return_value
    mock_response = MagicMock()
    mock_stub.RunScript.return_value = mock_response
    mock_response.result.result = "{'result': 'success'}"
    mock_response.log = MagicMock()
    mock_response.log.messages = [LogMessage(2, "Hello World!")]
    client.run_script_file(script_dir / "cooled_turbine_blade.py")
    mock_stub.RunScript.assert_called_once()
    assert mock_stub.RunScript.call_count == 1
    assert mock_response.result.result == "{'result': 'success'}"

    client._disconnect()
    with pytest.raises(Exception):
        client.run_script_file(script_dir / "cooled_turbine_blade.py")


def test_upload_file(mock_workbench_service_stub):
    """Test the upload_file method."""
    client = WorkbenchClient(local_workdir="/tmp", server_host="localhost", server_port=5000)
    client._connect()
    mock_stub = mock_workbench_service_stub.return_value
    mock_response = MagicMock()
    mock_response.error = None
    mock_response.file_name = "uploaded_file1"
    mock_stub.UploadFile.return_value = mock_response

    with patch("ansys.workbench.core.workbench_client.os.path.isfile", return_value=True):
        with patch(
            "ansys.workbench.core.workbench_client.glob.glob", return_value=["file1", "file2"]
        ):
            client.upload_file("file*", show_progress=True)
            assert mock_stub.UploadFile.call_count == 2


def test_upload_file_from_example_repo(mock_workbench_service_stub):
    """Test the upload_file_from_example_repo method."""
    client = WorkbenchClient(local_workdir="/tmp", server_host="localhost", server_port=5000)
    client._connect()
    mock_stub = mock_workbench_service_stub.return_value
    mock_response = MagicMock()
    mock_response.error = None
    mock_response.file_name = "uploaded_file1"
    mock_stub.UploadFile.return_value = mock_response

    with patch("ansys.workbench.core.workbench_client.os.path.isfile", return_value=True):
        with patch(
            "ansys.workbench.core.workbench_client.ExampleData.download",
            return_value="/tmp/axisymmetric_model.agdb",
        ):
            client.upload_file_from_example_repo(
                "axisymmetric-rotor/agdb/axisymmetric_model.agdb", show_progress=True
            )
            assert mock_stub.UploadFile.call_count == 1


def test_upload_iterator():
    """Test the __upload_iterator method."""
    with tempfile.NamedTemporaryFile(mode="wb", delete=False) as tmp_file:
        tmp_file.write(b"mock_file_content")

    try:
        # Create a WorkbenchClient instance
        client = WorkbenchClient(local_workdir="/tmp", server_host="localhost", server_port=5000)
        client._connect()

        # Get the temporary file path
        file_path = tmp_file.name

        # Call the method under test
        iterator = client._WorkbenchClient__upload_iterator(file_path, show_progress=True)

        # Assertions
        upload_requests = list(iterator)
        assert (
            len(upload_requests) > 1
        )  # Assuming the file is large enough to yield more than one chunk
    finally:
        # Clean up the temporary file
        if pathlib.Path(file_path).exists():
            pathlib.Path(file_path).unlink()


def test_download_file(mock_workbench_service_stub):
    """Test the download_file method."""
    client = WorkbenchClient(local_workdir="/tmp", server_host="localhost", server_port=5000)
    client._connect()
    mock_stub = mock_workbench_service_stub.return_value
    client.stub = mock_stub

    # Mock response setup
    mock_response_1 = MagicMock()
    mock_response_1.file_info = MagicMock()
    mock_response_1.error = None
    mock_response_1.file_info.is_archive = True
    mock_response_1.file_info.file_size = 200  # Let's assume the file size is 200 bytes
    mock_response_1.file_content = b"mock_file_content1"

    mock_response2 = MagicMock()
    mock_response2.file_content = b"mock_file_content2"

    with tempfile.NamedTemporaryFile(mode="wb", delete=False) as tmp_file:
        tmp_file.write(b"mock_file_content")
        file_path = tmp_file.name

    # Set up return value for the mock method
    mock_stub.DownloadFile.return_value = [mock_response_1, mock_response2]

    # Call the method under test
    with patch("ansys.workbench.core.workbench_client.os.path.isfile", return_value=False):
        client.download_file(file_path, target_dir="/tmp", show_progress=True)

    # Assertions
    assert mock_stub.DownloadFile.call_count == 1
    assert mock_response_1.file_info.file_size == 200  # Ensure the file size is set correctly
