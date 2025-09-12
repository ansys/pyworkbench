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

"""Tests for launch workbench client."""

import pathlib

import pytest

from ansys.workbench.core import launch_workbench


@pytest.fixture(scope="module")
def workbench():
    """Launch workbench."""
    workdir = pathlib.Path(__file__).parent
    wb = launch_workbench(
        version="251",
        client_workdir=str(workdir.absolute()),
    )
    yield wb
    wb.exit()


def test_launch_workbench(workbench):
    """Test launching workbench."""
    assert workbench is not None


def test_upload_file(workbench):
    """Test uploading a file."""
    assets = pathlib.Path("assets")
    workbench.upload_file(str(assets / "axisymmetric_model.agdb"))


def test_run_script(workbench):
    """Test running a script."""
    assets = pathlib.Path("assets")
    workbench.upload_file_from_example_repo("cooled-turbine-blade/wbpz/cooled_turbine_blade.wbpz")
    export_path = "wb_log_file.log"
    workbench.set_log_file(export_path)
    workbench.run_script_file(str(assets / "project.wbjn"), log_level="info")
    # workbench.download_file(file_name=export_path, target_dir=str(assets), show_progress=True)


def test_download_file(workbench):
    """Test downloading a file."""
    workbench.download_file("axisymmetric_model.agdb")
