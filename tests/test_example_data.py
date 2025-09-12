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

"""Tests for the example_data module."""

import pathlib

import pytest

from ansys.workbench.core.example_data import ExampleData


@pytest.fixture(scope="module")
def example_data():
    """Return example data."""
    file_name = "axisymmetric_model.agdb"
    dir_name = "axisymmetric-rotor/agdb"
    source_path = f"{dir_name}/{file_name}"
    target_local_dir = "tests/assets/"
    return source_path, target_local_dir


def test_get_file_url(example_data):
    """Test get_file_url."""
    source_path, target_local_dir = example_data
    url = ExampleData._get_file_url(relative_file_path=source_path)
    assert url == f"https://github.com/ansys/example-data/raw/master/pyworkbench/{source_path}"


def test_download(example_data):
    """Test download."""
    source_path, target_local_dir = example_data
    local_file_path = ExampleData.download(source_path, target_local_dir)
    local_file_dir = pathlib.Path(target_local_dir)
    local_file_path = pathlib.Path(local_file_dir / "axisymmetric_model.agdb")
    assert local_file_path.exists()
