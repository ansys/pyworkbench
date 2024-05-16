## ansys-workbench-core PyWorkbench Package

This Python package contains the public API to PyWorkbench.


### Installation

NOTE: Users must first apply the ``PYANSYS_PRIVATE_PYPI_PAT`` token as an environment variable.  This allows authentication with Private PyPI.
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


### Build

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


### Automatic Deployment

This repository contains GitHub CI/CD that enables the automatic building of
source and wheel packages for these gRPC Python interface files. By default,
these are built on PRs, the main branch, and on tags when pushing. Artifacts
are uploaded to GitHub for each PR and push to the main branch. Artifacts
are published to Ansys Private PyPI when tags are pushed.

To release wheels to PyPI, a release branch should be created with the version in `pyproject.toml` updated and a tag created.

For example, suppose the current main branch version is ``v0.3.dev0`` and it is time to release ``0.3.0`` to Private PyPI, the steps are:
1. create a new branch named ``release/0.3`` from the main branch;
while the main branch should remain at version ``0.3.dev0`` until the step 5.
2. in the ``release/0.3`` branch, update the version to reflect the release version ``0.3.0``;
3. after updating the version, tag the commit corresponding to this release version.
```bash
git tag v0.3.0
```
Note that there is a 'v' prepended to the GitHub tag, keeping with best practices.
The 'v' is not required in the `pyproject.toml` file.

4. push both the branch (``release/0.3``) and the tag to the remote repository.
```bash
git push
git push --tags
```
5. after completing the release process for version ``0.3.0``, the main branch can then be updated to reflect the next anticipated version, which is ``0.4.dev0``.
