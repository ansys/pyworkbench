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

"""Tests for the example_data module."""

import pathlib

import pytest

from ansys.workbench.core.example_data import ExampleData


@pytest.fixture(scope="module")
def example_data():
    """Return example data."""
    file_name = "axisymmetric_model.agdb"
    dir_name = "axisymmetric-rotor/agdb"
    relative_path = f"{dir_name}/{file_name}"
    assets_dir = "tests/assets/"
    return relative_path, assets_dir


def test_get_file_url(example_data):
    """Test get_file_url."""
    relative_path, asset_file = example_data
    url = ExampleData._get_file_url(relative_file_path=relative_path)
    assert url == f"https://github.com/ansys/example-data/raw/master/pyworkbench/{relative_path}"


def test_download(example_data):
    """Test download."""
    relative_path, asset_file = example_data
    local_file_path = ExampleData.download(relative_path, asset_file)
    local_file_path = pathlib.Path("tests/assets/axisymmetric_model.agdb")
    assert local_file_path.exists()
    local_file_path.unlink()
    assert not local_file_path.exists()
