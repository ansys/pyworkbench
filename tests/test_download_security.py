# Copyright (C) 2023 - 2026 ANSYS, Inc. and/or its affiliates.
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

"""Security regressions for downloads using mocked RPCs and isolated directories."""

import os
from pathlib import Path
import subprocess
from unittest.mock import MagicMock

import pytest

from ansys.api.workbench.v0 import workbench_pb2 as wb
import ansys.workbench.core.workbench_client as client_module
from ansys.workbench.core.workbench_client import WorkbenchClient


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Create a client without opening a channel or launching Ansys."""
    workdir = tmp_path / "downloads"
    workdir.mkdir()
    instance = WorkbenchClient(str(workdir), "localhost", 0, "mtls")
    instance.channel = MagicMock()
    instance.stub = MagicMock()
    instance.stub.DownloadFile.return_value = [wb.DownloadFileResponse(file_content=b"new data")]
    monkeypatch.setattr(instance, "run_script_string", MagicMock(return_value="server-info.txt"))
    return instance


@pytest.mark.parametrize(
    "filename",
    [
        "",
        None,
        123,
        [],
        {},
        ".",
        "..",
        "../outside.txt",
        "..\\outside.txt",
        "/outside.txt",
        "\\outside.txt",
        "C:\\outside.txt",
        "C:/outside.txt",
        "C:outside.txt",
        "\\\\server\\share\\outside.txt",
        "//server/share/outside.txt",
        "\\\\?\\C:\\outside.txt",
        "\\\\.\\NUL",
        "nested/info.txt",
        "nested\\info.txt",
        "file.txt:stream",
        "*.txt",
        "file?.txt",
        "bad\x00name",
        "bad\nname",
        "bad\rname",
        "bad\tname",
        "bad\x7fname",
        'bad"name',
        "bad|name",
        "bad<name",
        "bad>name",
        "trailing.",
        "trailing ",
        "NUL",
        "nul.txt",
        "NUL .txt",
        "CON",
        "PRN.log",
        "AUX",
        "COM1.txt",
        "LPT9",
        "COM¹.txt",
        "LPT².txt",
        "CONIN$",
        "CONOUT$",
    ],
)
def test_reject_server_filename_before_io(client, monkeypatch, filename):
    """Reject unsafe server names before requesting data or mutating local files."""
    client.run_script_string.return_value = filename
    remove = MagicMock()
    replace = MagicMock()
    temporary_file = MagicMock()
    monkeypatch.setattr(client_module.os, "remove", remove)
    monkeypatch.setattr(client_module.os, "replace", replace)
    monkeypatch.setattr(client_module.tempfile, "NamedTemporaryFile", temporary_file)

    with pytest.raises(ValueError):
        client.start_fluent_server("trusted-system")

    client.stub.DownloadFile.assert_not_called()
    remove.assert_not_called()
    replace.assert_not_called()
    temporary_file.assert_not_called()
    assert list(Path(client.workdir).iterdir()) == []


@pytest.mark.parametrize("absolute", [False, True])
def test_server_path_cannot_delete_existing_outside_file(client, tmp_path, absolute):
    """Keep an existing outside file intact even when the server supplies its name."""
    outside = tmp_path / "outside.txt"
    outside.write_bytes(b"original")
    client.run_script_string.return_value = str(outside) if absolute else "../outside.txt"

    with pytest.raises(ValueError):
        client.start_fluent_server("trusted-system")

    assert outside.read_bytes() == b"original"
    client.stub.DownloadFile.assert_not_called()


@pytest.mark.parametrize("filename", ["server-info.txt", "résultats 模型 (1).txt", "COM10.txt"])
def test_server_download_replaces_only_after_success(client, filename):
    """Allow portable names and retain the original until every chunk is received."""
    destination = Path(client.workdir) / filename
    destination.write_bytes(b"original")
    client.run_script_string.return_value = filename

    def responses():
        yield wb.DownloadFileResponse(file_info=wb.DownloadFileInfo(file_size=8))
        assert destination.read_bytes() == b"original"
        yield wb.DownloadFileResponse(file_content=b"new ")
        assert destination.read_bytes() == b"original"
        yield wb.DownloadFileResponse(file_content=b"data")
        assert destination.read_bytes() == b"original"

    client.stub.DownloadFile.return_value = responses()
    assert client.start_fluent_server("trusted-system") == str(destination)
    assert destination.read_bytes() == b"new data"
    assert set(Path(client.workdir).iterdir()) == {destination}
    assert client.stub.DownloadFile.call_args.args[0].file_name == filename
    if os.name != "nt":
        assert destination.stat().st_mode & 0o077 == 0


@pytest.mark.parametrize("failure", ["server-error", "rpc-error", "empty-stream", "archive"])
@pytest.mark.parametrize("existing", [False, True])
def test_server_download_failure_preserves_destination(client, failure, existing):
    """Do not publish partial files or return a path to stale connection information."""
    destination = Path(client.workdir) / "server-info.txt"
    if existing:
        destination.write_bytes(b"original")

    def responses():
        if failure == "empty-stream":
            return
        yield wb.DownloadFileResponse(file_content=b"partial")
        if failure == "rpc-error":
            raise RuntimeError("RPC interrupted")
        if failure == "archive":
            yield wb.DownloadFileResponse(file_info=wb.DownloadFileInfo(is_archive=True))
        else:
            yield wb.DownloadFileResponse(error="transfer failed")

    client.stub.DownloadFile.return_value = responses()
    if failure in {"rpc-error", "archive"}:
        with pytest.raises(RuntimeError if failure == "rpc-error" else ValueError):
            client.start_fluent_server("trusted-system")
    else:
        assert client.start_fluent_server("trusted-system") is None

    if existing:
        assert destination.read_bytes() == b"original"
    else:
        assert not destination.exists()
    assert set(Path(client.workdir).iterdir()) == ({destination} if existing else set())


@pytest.mark.parametrize("dangling", [False, True])
def test_reject_outside_symlink(client, tmp_path, dangling):
    """Reject existing and dangling symlinks that escape the working directory."""
    outside = tmp_path / "outside.txt"
    if not dangling:
        outside.write_bytes(b"original")
    link = Path(client.workdir) / "server-info.txt"
    try:
        link.symlink_to(outside)
    except (OSError, NotImplementedError):
        pytest.skip("Creating symlinks is not available for this account")

    with pytest.raises(ValueError, match="outside"):
        client.start_fluent_server("trusted-system")

    assert link.is_symlink()
    assert outside.read_bytes() == b"original" if not dangling else not outside.exists()
    client.stub.DownloadFile.assert_not_called()
    assert set(Path(client.workdir).iterdir()) == {link}


@pytest.mark.skipif(os.name != "nt", reason="Windows directory junctions only")
def test_reject_outside_junction(client, tmp_path):
    """Reject a Windows junction without touching the directory it points to."""
    outside = tmp_path / "outside"
    outside.mkdir()
    marker = outside / "marker.txt"
    marker.write_bytes(b"original")
    junction = Path(client.workdir) / "server-info.txt"
    subprocess.run(
        ["cmd.exe", "/d", "/c", "mklink", "/J", str(junction), str(outside)],
        check=True,
        capture_output=True,
    )
    try:
        with pytest.raises(ValueError, match="outside"):
            client.start_fluent_server("trusted-system")
        assert marker.read_bytes() == b"original"
        client.stub.DownloadFile.assert_not_called()
    finally:
        junction.rmdir()


def test_recheck_containment_before_publication(client, tmp_path, monkeypatch):
    """Recheck resolved destinations if a symlink or junction changes mid-transfer."""
    destination = Path(client.workdir) / "server-info.txt"
    destination.write_bytes(b"original")
    outside = tmp_path / "outside.txt"
    outside.write_bytes(b"outside")
    realpath = os.path.realpath
    redirected = False

    def resolve(path, *args, **kwargs):
        if redirected and os.fspath(path) == str(destination):
            return str(outside)
        return realpath(path, *args, **kwargs)

    def responses():
        nonlocal redirected
        yield wb.DownloadFileResponse(file_content=b"new data")
        redirected = True

    monkeypatch.setattr(client_module.os.path, "realpath", resolve)
    client.stub.DownloadFile.return_value = responses()
    with pytest.raises(ValueError, match="outside"):
        client.start_fluent_server("trusted-system")
    assert destination.read_bytes() == b"original"
    assert outside.read_bytes() == b"outside"
    assert set(Path(client.workdir).iterdir()) == {destination}


@pytest.mark.parametrize("failures", [1, 3])
def test_atomic_replace_retries_and_cleans_up(client, monkeypatch, failures):
    """Retry transient Windows sharing errors and propagate persistent failures."""
    destination = Path(client.workdir) / "server-info.txt"
    destination.write_bytes(b"original")
    real_replace = os.replace
    attempts = 0

    def replace(source, target):
        nonlocal attempts
        attempts += 1
        assert destination.read_bytes() == b"original"
        assert Path(source).parent == destination.parent
        if attempts <= failures:
            raise PermissionError("file is locked")
        return real_replace(source, target)

    monkeypatch.setattr(client_module.os, "replace", replace)
    monkeypatch.setattr(client_module.time, "sleep", MagicMock())
    if failures == 3:
        with pytest.raises(PermissionError):
            client.start_fluent_server("trusted-system")
        assert destination.read_bytes() == b"original"
        assert attempts == 3
    else:
        assert client.start_fluent_server("trusted-system") == str(destination)
        assert destination.read_bytes() == b"new data"
        assert attempts == 2
    assert set(Path(client.workdir).iterdir()) == {destination}


@pytest.mark.parametrize("destination_kind", ["absolute", "target-dir", "parent-relative"])
def test_caller_destinations_are_confined(client, tmp_path, destination_kind):
    """Public downloads keep only the base name and write inside the target directory."""
    outside = tmp_path / "caller-selected.txt"
    outside.write_bytes(b"original")
    target_dir = None
    if destination_kind == "absolute":
        filename = str(outside)
    elif destination_kind == "target-dir":
        filename = outside.name
        target_dir = tmp_path
    else:
        filename = "../caller-selected.txt"

    result = client.download_file(filename, show_progress=False, target_dir=target_dir)
    assert result == "caller-selected.txt"
    if target_dir is None:
        assert outside.read_bytes() == b"original"
        assert (Path(client.workdir) / result).read_bytes() == b"new data"
    else:
        assert outside.read_bytes() == b"new data"
        assert list(Path(client.workdir).iterdir()) == []
    assert client.stub.DownloadFile.call_args.args[0].file_name == filename


def test_wildcard_archive_download(client):
    """Preserve wildcard requests and append the ZIP suffix only once."""
    info = wb.DownloadFileResponse(file_info=wb.DownloadFileInfo(is_archive=True, file_size=8))
    client.stub.DownloadFile.return_value = [
        info,
        wb.DownloadFileResponse(file_content=b"new "),
        info,
        wb.DownloadFileResponse(file_content=b"data"),
    ]
    assert client.download_file("result?.*", show_progress=False) == "result_._.zip"
    destination = Path(client.workdir) / "result_._.zip"
    assert destination.read_bytes() == b"new data"
    assert set(Path(client.workdir).iterdir()) == {destination}
    assert client.stub.DownloadFile.call_args.args[0].file_name == "result?.*"


def test_zero_length_download(client):
    """Publish an empty file when the server explicitly reports a zero-length file."""
    destination = Path(client.workdir) / "empty.txt"
    destination.write_bytes(b"original")
    client.stub.DownloadFile.return_value = [
        wb.DownloadFileResponse(file_info=wb.DownloadFileInfo(file_size=0))
    ]
    assert client.download_file("empty.txt", show_progress=False) == "empty.txt"
    assert destination.read_bytes() == b""


def test_progress_closed_on_failure(client, monkeypatch):
    """Close progress reporting and remove staging files on server errors."""
    progress = MagicMock()
    monkeypatch.setattr(client_module.tqdm, "tqdm", MagicMock(return_value=progress))
    client.stub.DownloadFile.return_value = [
        wb.DownloadFileResponse(file_info=wb.DownloadFileInfo(file_size=100)),
        wb.DownloadFileResponse(file_content=b"partial"),
        wb.DownloadFileResponse(error="transfer failed"),
    ]
    assert client.download_file("result.txt") is None
    progress.update.assert_called_once_with(7)
    progress.close.assert_called_once()
    assert list(Path(client.workdir).iterdir()) == []