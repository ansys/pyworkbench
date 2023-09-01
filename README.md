# ansys-workbench-core PyWorkbench Package

This Python package contains the public API to PyWorkbench.


## Installation

NOTE: Users must first apply the `PYANSYS_PRIVATE_PYPI_PAT` token as an environment variable.  This allows authentication with Private PyPI.
The value can be found at the following [link](https://dev-docs.solutions.ansys.com/solution_journey/journey_prepare/connect_to_private_pypi.html).

Provided that these wheels have been published to PyPI, they can be
installed with:

Linux (bash)
```bash
# Create and activate a virtualenv
python -m venv .venv
source .venv/bin/activate  # can be deactivated with the 'deactivate' command
# Install pre-requisites to connect to artifact feed
pip install --upgrade pip
pip install keyring artifacts-keyring
#Install wMI (Not Available in Private PyPI At This Time)
pip install wMI==1.5.1
# Install the latest package
pip install --index-url https://$PYANSYS_PRIVATE_PYPI_PAT@pkgs.dev.azure.com/pyansys/_packaging/pyansys/pypi/simple ansys-workbench-core
# OR - Install a package version of your choice
pip install --index-url https://$PYANSYS_PRIVATE_PYPI_PAT@pkgs.dev.azure.com/pyansys/_packaging/pyansys/pypi/simple ansys-workbench-core==0.1.2
```

Windows (PowerShell)
```powershell
# Create and activate a virtualenv
python.exe -m venv .venv
.\venv\Scripts\Activate.ps1  # can be deactivated with the 'deactivate' command
# Install pre-requisites to connect to artifact feed
pip.exe install --upgrade pip
pip.exe install keyring artifacts-keyring
#Install wMI (Not Available in Private PyPI At This Time)
pip.exe install wMI==1.5.1
# Install the latest package
pip.exe install --index-url https://$env:PYANSYS_PRIVATE_PYPI_PAT@pkgs.dev.azure.com/pyansys/_packaging/pyansys/pypi/simple ansys-workbench-core
# OR - Install a package version of your choice
pip.exe install --index-url https://$env:PYANSYS_PRIVATE_PYPI_PAT@pkgs.dev.azure.com/pyansys/_packaging/pyansys/pypi/simple ansys-workbench-core==0.1.2
```

Windows (Command Prompt)
```
# Create and activate a virtualenv
python -m venv .venv
.\venv\Scripts\activate.bat  # can be deactivated with the 'deactivate' command
# Install pre-requisites to connect to artifact feed
pip install --upgrade pip
pip install keyring artifacts-keyring
#Install wMI (Not Available in Private PyPI At This Time)
pip install wMI==1.5.1
# Install the latest package
pip install --index-url https://%PYANSYS_PRIVATE_PYPI_PAT%@pkgs.dev.azure.com/pyansys/_packaging/pyansys/pypi/simple ansys-workbench-core
# OR - Install a package version of your choice
pip install --index-url https://%PYANSYS_PRIVATE_PYPI_PAT%@pkgs.dev.azure.com/pyansys/_packaging/pyansys/pypi/simple ansys-workbench-core==0.1.2
```


## Build

To build the gRPC packages, run:

```
pip install build
python -m build
```

This will create both the source distribution containing just the protofiles
along with the wheel containing the protofiles and build Python interface
files.

Note that the interface files are identical regardless of the version of Python
used to generate them, but the last pre-built wheel for ``grpcio~=1.17`` was
Python 3.7, so to improve your build time, use Python 3.7 when building the
wheel.


## Automatic Deployment

This repository contains GitHub CI/CD that enables the automatic building of
source and wheel packages for these gRPC Python interface files. By default,
these are built on PRs, the main branch, and on tags when pushing. Artifacts
are uploaded to GitHub for each PR and push to the main branch.  Artifacts
are published to Ansys Private PyPI when tags are pushed.

To release wheels to PyPI, ensure your branch is up-to-date and then
push tags. For example, for the version ``v0.1.5``.  This version MUST MATCH
the version in `pyproject.toml`.

For example, if you intend to release version `0.1.5` to Private PyPI, the
pyproject.toml file should contain '0.1.5'.  You will then run:

```bash
git tag v0.1.5
git push --tags
```

Note that there is a 'v' prepended to the GitHub tag, keeping with best practices.
The 'v' is not required in the `pyproject.toml` file.
