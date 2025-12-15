Install PyWorkbench locally in Windows
######################################

This page explains how to install PyWorkbench locally on a Windows platform.

.. note::

    The following instructions assume that you have a local installation of Workbench and a valid
    license in your machine.

There are two ways to install PyWorkbench on Windows:

* `Install from PyPI <Install from PyPI_>`_
* `Download artifacts <Download artifacts_>`_

Install from PyPI
=================

PyWorkbench is available on the `Python Package Index (PyPI) <https://pypi.org/project/ansys-workbench/>`_.
You can install PyWorkbench using this `pip <https://pypi.org/project/pip/>`_ command:

.. code-block:: shell

  python -m pip install ansys-workbench-core

Verify the installation by running this code:

.. code-block:: python

    from ansys.workbench.core import launch_workbench

    launch_workbench()

Download artifacts
==================

Start by downloading PyWorkbench wheel or source artifacts for Windows. Wheel artifacts
are the preferred option for installing PyWorkbench.

.. jinja:: artifacts

    .. tab-set::
        :sync-group: artifacts

        .. tab-item:: **Wheels download**
            :sync: wheels

            Wheel artifacts for installing PyWorkbench:

            .. list-table::
                :widths: auto

                * - **Artifact**
                  - `{{ wheels }} <../../_static/artifacts/{{ wheels }}>`_
                * - **Size**
                  - {{ wheels_size }}
                * - **SHA-256**
                  - {{ wheels_hash }}

        .. tab-item:: **Source download**
            :sync: source

            Source distribution for installing PyWorkbench:

            .. list-table::
                :widths: auto

                * - **Artifact**
                  - `{{ source }} <../../_static/artifacts/{{ source }}>`_
                * - **Size**
                  - {{ source_size }}
                * - **SHA-256**
                  - {{ source_hash }}

Install artifacts
=================

Install Windows artifacts by using the `pip <https://pypi.org/project/pip/>`_ command:

.. jinja:: artifacts

    .. tab-set::
        :sync-group: artifacts

        .. tab-item:: **Wheels install**
            :sync: wheels

            .. code-block:: text

                python -m pip install {{ wheels }}

        .. tab-item:: **Source install**
            :sync: source

            .. code-block:: text

                python -m pip install {{ source }}

Verify installation
===================

Verify a successful installation of PyWorkbench by running:

.. jinja::

    .. code-block:: python

        from ansys.workbench.core import launch_workbench


        launch_workbench()
