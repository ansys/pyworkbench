Install PyWorkbench locally in Linux
####################################

This guideline covers the local installation of PyWorkbench in Linux platforms.

.. note::

    This guide assumes that you have a local installation of STK and a valid
    license in your machine.

Download artifacts
==================

Start by downloading PyWorkbench wheel or source artifacts for Linux:

.. jinja:: artifacts

    .. tab-set::
        :sync-group: artifacts

        .. tab-item:: **Wheels download**
            :sync: wheels

            Wheel artifacts are the preferred option for installing PyWorkbench:

            .. list-table::
                :widths: auto

                * - **Artifact**
                  - `{{ wheels }} <../../../_static/artifacts/{{ wheels }}>`_
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
                  - `{{ source }} <../../../_static/artifacts/{{ source }}>`_
                * - **Size**
                  - {{ source_size }}
                * - **SHA-256**
                  - {{ source_hash }}

Install artifacts
=================

Install Linux artifacts by using the `pip <https://pypi.org/project/pip/>`_ command:

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
