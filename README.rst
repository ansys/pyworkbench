ansys-workbench-core PyWorkbench Package
========================================

|pyansys| |python| |pypi| |GH-CI| |MIT| |ruff|

.. |pyansys| image:: https://img.shields.io/badge/Py-Ansys-ffc107.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAABDklEQVQ4jWNgoDfg5mD8vE7q/3bpVyskbW0sMRUwofHD7Dh5OBkZGBgW7/3W2tZpa2tLQEOyOzeEsfumlK2tbVpaGj4N6jIs1lpsDAwMJ278sveMY2BgCA0NFRISwqkhyQ1q/Nyd3zg4OBgYGNjZ2ePi4rB5loGBhZnhxTLJ/9ulv26Q4uVk1NXV/f///////69du4Zdg78lx//t0v+3S88rFISInD59GqIH2esIJ8G9O2/XVwhjzpw5EAam1xkkBJn/bJX+v1365hxxuCAfH9+3b9/+////48cPuNehNsS7cDEzMTAwMMzb+Q2u4dOnT2vWrMHu9ZtzxP9vl/69RVpCkBlZ3N7enoDXBwEAAA+YYitOilMVAAAAAElFTkSuQmCC
   :target: https://docs.pyansys.com/
   :alt: PyAnsys

.. |python| image:: https://img.shields.io/pypi/pyversions/ansys-workbench-core?logo=pypi
   :target: https://pypi.org/project/ansys-workbench-core/
   :alt: Python

.. |pypi| image:: https://img.shields.io/pypi/v/ansys-workbench-core.svg?logo=python&logoColor=white
   :target: https://pypi.org/project/ansys-workbench-core
   :alt: PyPI

.. |GH-CI| image:: https://github.com/ansys-internal/pyworkbench/actions/workflows/ci_cd.yml/badge.svg
   :target: https://github.com/ansys-internal/pyworkbench/actions/workflows/ci_cd.yml
   :alt: GH-CI

.. |MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/blog/license/mit
   :alt: MIT

.. |ruff| image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Ruff

This Python package contains the public API to PyWorkbench.

Installation
------------

.. note::

    Users must first apply the ``PYANSYS_PRIVATE_PYPI_PAT`` token as an environment variable.
    This allows authentication with Private PyPI.
    The value can be found at the following `link<https://dev-docs.solutions.ansys.com/solution_journey/journey_prepare/connect_to_private_pypi.html>`_.

Provided that these wheels have been published to PyPI, they can be
installed with:

Linux (bash)

.. code::

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


Windows (PowerShell)

.. code::bash

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

Documentation
-------------

Documentation of the latest stable release of PyWorkbench can be found at
PyWorkbench Documentation <https://workbench.docs.pyansys.com>`_.

The documentation has these sections:

- `Installation <https://workbench.docs.pyansys.com/version/stable/installation.html>`_
- `User Guide <https://workbench.docs.pyansys.com/version/stable/user_guide.html>`_
- `API Reference <https://workbench.docs.pyansys.com/version/stable/api/index.html>`_
- `contribute <https://workbench.docs.pyansys.com/version/stable/contribute_examples.html>`_


In the upper right corner of the documentation's title bar, there is an option for switching from
viewing the documentation for the
latest stable release to viewing the documentation for the development version or previously released versions.

On the `PyWorkbench <https://github.com/ansys-internal/pyworkbench/issues>`_
page, you can create issues to report bugs and request new features. On the
`Discussions <https://discuss.ansys.com/>`_ page on the Ansys Developer portal,
you can post questions, share ideas, and get community feedback.

If you have general questions about the PyAnsys ecosystem, email
`pyansys.core@ansys.com <pyansys.core@ansys.com>`_. If your
question is specific to PyWorkbench, ask your
question in an issue as described in the previous paragraph.

