Install PyWorkbench
###################

Installing PyWorkbench is as simple as installing any Python library. However, you must
have a running instance of Workbench to use PyWorkbench.

PyWorkbech has two installation modes: user and developer.

Install in user mode
====================

You can install PyWorkbench in user mode from PyPI sources using ``pip`` or from the
GitHub repository:

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

Install in developer mode
=========================

Developer installation is specifically intended for project maintainers. This
specialized installation is tailored to equip developers with the essential
tools and resources required for effective contribution to the project's
development and maintenance. The developer installation assumes a certain level
of technical expertise and familiarity with the project's codebase, rendering it
most suitable for individuals actively engaged in its continuous development and
maintenance.

#. Cloning the repository:

   .. code-block::

       git clone git@github.com:ansys/pyworkbench


#. Move inside the project and create a clean Python environment:

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

#. Activate the environment:

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

#. Install the project in editable mode, which means that any changes you make to
   the package's source code is immediately reflected in your project without requiring you
   to reinstall it.

   .. code-block::

       python -m pip install --editable .


Verify your installation
========================

If Ansys Workbench is installed locally, you can verify your PyWorkbench
installation by starting a Workbench server session on your local machine:

.. code-block:: python

    from ansys.workbench.core import launch_workbench

    workbench = launch_workbench()
