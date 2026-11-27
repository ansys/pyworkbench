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

"""Tests for workbench launcher."""

from ansys.workbench.core.workbench_launcher import Launcher


class MissingWmiProcess:
    """Represent a terminated WMI process object."""

    def __init__(self, process_name=None):
        self.Name = process_name

    @property
    def ProcessId(self):
        """Raise because the WMI process no longer exists."""
        raise RuntimeError("ProcessId is unavailable")

    @property
    def pid(self):
        """Raise because WMI objects do not expose pid safely here."""
        raise RuntimeError("pid is unavailable")

    def Terminate(self):
        """Raise because the process is already gone."""
        raise RuntimeError("process not found")


def test_exit_handles_missing_wmi_process():
    """Ensure exit does not fail when the launched WMI process already exited."""
    launcher = object.__new__(Launcher)
    launcher._wmi = object()
    launcher._libc = None
    launcher._wmi_connection = object()
    launcher._process_id = 61358
    launcher._process = MissingWmiProcess("RunWB2.exe")
    launcher._Launcher__collect_process_tree = lambda: []

    launcher.exit()

    assert launcher._wmi_connection is None
    assert launcher._process_id == -1
    assert launcher._process is None


def test_describe_process_uses_available_name_when_ids_fail():
    """Use the process name when id lookups fail with runtime exceptions."""
    launcher = object.__new__(Launcher)
    launcher._process_id = 61358

    assert launcher._Launcher__describe_process(MissingWmiProcess("RunWB2.exe")) == "RunWB2.exe"


def test_describe_process_does_not_use_parent_id_for_child_process():
    """Return an unknown label when a child process cannot describe itself."""
    launcher = object.__new__(Launcher)
    launcher._process_id = 61358

    assert launcher._Launcher__describe_process(MissingWmiProcess()) == "unknown process"


def test_describe_process_uses_explicit_fallback_process_id():
    """Use the explicit fallback for the launched process description only."""
    launcher = object.__new__(Launcher)
    launcher._process_id = 61358

    assert launcher._Launcher__describe_process(
        MissingWmiProcess(), fallback_process_id=launcher._process_id
    ) == "61358"
