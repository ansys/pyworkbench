Getting started
###############

Installing PyWorkbench is as simple as installing a Python library. However, a running
instance of Workbench is required to use PyWorkbench.

User installation
=================

There are multiple sources for installing the latest stable version of
PyWorkbench. These include ``pip`` and ``GitHub``.

.. jinja:: install_guide

    .. tab-set::

        .. tab-item:: Public PyPI

            .. code-block::

                python -m pip install ansys-workbench-core

        .. tab-item:: Ansys PyPI

            .. code-block::

                export TWINE_USERNAME="__token__"
                export TWINE_REPOSITORY_URL="https://pkgs.dev.azure.com/pyansys/_packaging/pyansys/pypi/upload"
                export TWINE_PASSWORD=***
                python -m pip install ansys-workbench-core

        .. tab-item:: GitHub

            .. code-block::

                python -m pip install git+https://github.com/ansys/pyworkbench.git@{{ version }}

Developer installation
======================

Developer installation is specifically intended for project maintainers. This
specialized installation is tailored to equip developers with the essential
tools and resources required for effective contribution to the project's
development and maintenance. The developer installation assumes a certain level
of technical expertise and familiarity with the project's codebase, rendering it
most suitable for individuals actively engaged in its continuous development and
maintenance.

Start by cloning the repository

.. code-block::

    git clone git@github.com:ansys/pyworkbench


Move inside the project and create a new Python environment:

.. tab-set::

    .. tab-item:: Windows

        .. tab-set::

            .. tab-item:: CMD

                .. code-block:: text

                    py -m venv <venv>

            .. tab-item:: PowerShell

                .. code-block:: text

                    py -m venv <venv>

    .. tab-item:: Linux/UNIX

        .. code-block:: text

            python -m venv <venv>

Activate previous environment:

.. tab-set::

    .. tab-item:: Windows

        .. tab-set::

            .. tab-item:: CMD

                .. code-block:: text

                    <venv>\Scripts\activate.bat

            .. tab-item:: PowerShell

                .. code-block:: text

                    <venv>\Scripts\Activate.ps1

    .. tab-item:: Linux/UNIX

        .. code-block:: text

            source <venv>/bin/activate

Install the project in editable mode. This means that any changes you make to
the package's source code immediately reflect in your project without requiring you
to reinstall it.

.. code-block::

    python -m pip install --editable .


Verify your installation
========================

If you have Ansys Workbench installed locally, you can verify your PyWorkbench
installation by starting a Workbench server session on your local computer:

.. code-block:: python

    from ansys.workbench.core import launch_workbench

    workbench = launch_workbench()
