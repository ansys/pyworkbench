Installation
============
The ``ansys.workbench.core`` package supports Python 3.8 through
Python 3.11 on Windows, Linux, and Mac.

You should consider installing PyWorkbench in a virtual environment.
For more information, see Python's
[venv -- Creation of virtual environments](https://docs.python.org/3/library/venv.html).

Install the latest package from [Ansys private PyPi](https://dev-docs.solutions.ansys.com/solution_journey/journey_prepare/connect_to_private_pypi.html) with this command:

bash
```
pip install --index-url https://$PYANSYS_PRIVATE_PYPI_PAT@pkgs.dev.azure.com/pyansys/_packaging/pyansys/pypi/simple ansys-workbench-core
```

PowerShell
```
pip.exe install --index-url https://$env:PYANSYS_PRIVATE_PYPI_PAT@pkgs.dev.azure.com/pyansys/_packaging/pyansys/pypi/simple ansys-workbench-core
```

Windows Command Prompt
```
pip install --index-url https://%PYANSYS_PRIVATE_PYPI_PAT%@pkgs.dev.azure.com/pyansys/_packaging/pyansys/pypi/simple ansys-workbench-core
```

where the environment variable ``PYANSYS_PRIVATE_PYPI_PAT`` contains Ansys Private PyPI authentication token.

Verify your installation
------------------------
If you have Ansys Workbench installed locally, you can verify your PyWorkbench
installation by starting a Workbench server session on your local computer:

```
    >>> from ansys.workbench.core import launch_workbench
    >>> wb = launch_workbench()
```
