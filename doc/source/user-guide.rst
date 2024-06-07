User guide
##########

This section provides an overview of the PyWorkbench package, explaining
key concepts and approaches when working with the Workbench gRPC service.

Start Workbench client and connect to a running Workbench server
================================================================

A typical user of the Workbench gRPC service starts a Workbench client that connects to
a running Workbench server on the cloud, given the server's name/IP and port.

.. code-block:: python

    from ansys.workbench.core.workbench_client import connect_workbench

    host = "server_machine_name_or_IP"
    port = server_port_number
    wb = connect_workbench(host=host, port=port)

Other options to the ``connect_workbench`` API include specifying a working directory for the client instead of using the default directory.

Launch Workbench server and start a client
==========================================

During the development phase or for debugging purposes, it is useful to start the Workbench server on the developer's desktop or some computer within the company network.

One can always start a Workbench server by executing the command `StartServer()` in any running Workbench session and use the returned server port to start a client, like in the example above.

Alternatively, one can launch a Workbench server and start a client programmatically in a client-side Python script. To launch a server on the local computer:

.. code-block:: python

    from ansys.workbench.core import launch_workbench

    wb = launch_workbench()

or to launch a server on a remote Windows machine with valid user credentials:

.. code-block:: python

    from ansys.workbench.core import launch_workbench

    host = "server_machine_name_or_ip"
    username = "your_username_on_server_machine"
    password = "your_password_on_server_machine"
    wb = launch_workbench(host=host, username=username, password=password)

Other options to the ``launch_workbench`` API include specifying a particular Workbench release to launch, specifying working directories on the server and/or the client instead of using the default directories.

.. code-block:: python

    from ansys.workbench.core import launch_workbench

    wb = launch_workbench(
        release="241",
        server_workdir="path_to_a_dir_on_server",
        client_workdir="path_to_a_dir_on_client",
    )

Run script/commands/queries on Workbench server
===============================================

IronPython based Workbench scripts containing commands/queries can be executed on the server via:

* `run_script_file`, which executes a script file in the client working directory; or
* `run_script_string`, which executes a script contained in the given string.

Any output that needs to be returned from these APIs can be assigned to the global variable `wb_script_result` in the script as a JSON string. For example, the following Workbench script returns all message summaries from the Workbench session:

.. code-block:: python

    import json

    messages = [m.Summary for m in GetMessages()]
    wb_script_result = json.dumps(messages)

These run_script APIs can also be called with different logging levels. The default logging level is 'error'. The following line will output to the logger all info/warnings/errors during the script run.

.. code-block:: python

    wb.run_script_file("a_script_file_name", log_level="info")

File handling
=============

Data files can be uploaded to the server or downloaded from the server, using `upload_file` or `download_file` API. The client-side working directory is used to hold these files unless absolute paths or target directories are specified. There is also a working directory on the server for the same purpose. The server's working directory can be obtained via the Workbench query `GetServerWorkingDirectory()` that runs on the server.

For example, this uploads all part files with a given prefix and all agdb files in the working directory, plus another file outside of the working directory, from client to server:

.. code-block:: python

    wb.upload_file("model?.prt", "*.agdb", "/path/to/some/file")

The following server-side Workbench script loads an uploaded geometry file from the server's working directory into a newly created Workbench system:

.. code-block:: python

    wb.run_script_string(
        r"""import os
    work_dir = GetServerWorkingDirectory()
    geometry_file = os.path.join(work_dir, "2pipes.agdb")
    template = GetTemplate(TemplateName="Static Structural", Solver="ANSYS")
    system = CreateSystemFromTemplate(Template=template, Name="Static Structural (ANSYS)")
    system.GetContainer(ComponentName="Geometry").SetFile(FilePath=geometry_file)
    """
    )

The following server-side Workbench script copies a Mechanical solver output file to the server's working directory to be downloaded later:

.. code-block:: python

    wb.run_script_string(
        r"""import os
    import shutil
    work_dir = GetServerWorkingDirectory()
    mechanical_dir = mechanical.project_directory
    out_file_src = os.path.join(mechanical_dir, "solve.out")
    out_file_des = os.path.join(work_dir, "solve.out")
    shutil.copyfile(out_file_src, out_file_des)
    """
    )

This client script downloads all files with .out extension from the server's working directory:

.. code-block:: python

    wb.download_file("*.out")

There is a special client API to upload a data file from `the ANSYS example database <https://github.com/ansys/example-data/tree/master/pyworkbench>`_ directly to the Workbench server. The file path relative to the pyworkbench folder in the database should be specified:

.. code-block:: python

    client.upload_file_from_example_repo("pymechanical-integration/agdb/two_pipes.agdb")

All the file handling APIs come with a progress bar that is shown by default. One can turn off the progress bar with an optional argument:

.. code-block:: python

    wb.download_file("solve.out", show_progress=False)

Start other PyANSYS services from systems in a PyWorkbench project
==================================================================

PyMechanical
------------

For any mechanical system in the Workbench project, the PyMechanical service can be started and connected to from the same client machine.
The following runs a server-side script to create a mechanical system, then starts the PyMechanical service for the system and establishes a PyMechanical client.

.. code-block:: python

    from ansys.mechanical.core import launch_mechanical

    sys_name = wb.run_script_string(
        r"""import json
    wb_script_result=json.dumps(GetTemplate(TemplateName="Static Structural (ANSYS)").CreateSystem().Name)
    """
    )
    server_port = wb.start_mechanical_server(system_name=sys_name)
    mechanical = launch_mechanical(start_instance=False, ip="localhost", port=server_port)

PyFluent
--------

This example illustrates how to start the PyFluent service and client for a Fluent system created in Workbench.

.. code-block:: python

    import ansys.fluent.core as pyfluent

    sys_name = wb.run_script_string(
        r"""import json
    wb_script_result=json.dumps(GetTemplate(TemplateName="FLUENT").CreateSystem().Name)
    """
    )
    server_info_file = wb.start_fluent_server(system_name=sys_name)
    fluent = pyfluent.connect_to_fluent(server_info_file_name=server_info_file)

PySherlock
----------

This example illustrates how to start the PySherlock service and client for a Sherlock system created in Workbench.

.. code-block:: python

    from ansys.sherlock.core import launcher as pysherlock

    sys_name = wb.run_script_string(
        r"""import json
    wb_script_result=json.dumps(GetTemplate(TemplateName="SherlockPre").CreateSystem().Name)
    """
    )
    server_port = wb.start_sherlock_server(system_name=sys_name)
    sherlock = pysherlock.connect_grpc_channel(port=server_port)
