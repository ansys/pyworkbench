User guide
##########

This section explains key concepts and approaches for using PyWorkbench
with the Workbench gRPC service.

Start Workbench client and connect to a running Workbench server
================================================================

To start a Workbench client that connects to a running Workbench server on the cloud, you
must provide the following information:

- Port number
- Server name or IP address, which is an optional parameter and when not specified, localhost is used
- Client-side working directory, which is an optional parameter indicating the default location for client-side files

.. code-block:: python

    from ansys.workbench.core import connect_workbench

    host = "server_machine_name_or_IP"
    port = server_port_number
    wb = connect_workbench(host=host, port=port)

The ``client_workdir`` parameter for the ``connect_workbench()`` function specifies a working
directory for the client instead of using the default directory.

Launch Workbench server and start a client
==========================================

During the development phase or when debugging, it is useful to start the
Workbench server on your desktop or some computer within the company network.

You can always start a Workbench server by running the ``StartServer()`` command
in any Workbench session. You then use the returned server port to start a client,
like in the preceding example.

Alternatively, you can launch a Workbench server and start a client programmatically in a
client-side Python script.

This code launches a server on a local Windows machine:

.. code-block:: python

    from ansys.workbench.core import launch_workbench

    wb = launch_workbench()

This code launches a server on a remote Windows machine with valid user credentials:

.. code-block:: python

    from ansys.workbench.core import launch_workbench

    host = "server_machine_name_or_ip"
    username = "your_username_on_server_machine"
    password = "your_password_on_server_machine"
    wb = launch_workbench(host=host, username=username, password=password)

Other options for the ``launch_workbench()`` function include specifying a particular
Workbench release to launch and specifying working directories on the server and/or the
client instead of using the default directories:

.. code-block:: python

    from ansys.workbench.core import launch_workbench

    wb = launch_workbench(
        release="242",
        server_workdir="path_to_a_dir_on_server",
        client_workdir="path_to_a_dir_on_client",
    )

Run scripts on Workbench server
===============================

You can use these methods to run IronPython-based Workbench scripts, which contain commands or
queries, with PyWorkbench:

- ``run_script_file``: Runs a script file in the client working directory.
- ``run_script_string``: Runs a script contained in the given string.

To the ``wb_script_result`` global variable in the script, you can assign any output that needs
to be returned from these methods, as a JSON string. For example, this Workbench script returns
all message summaries from the Workbench session:

.. code-block:: python

    import json

    messages = [m.Summary for m in GetMessages()]
    wb_script_result = json.dumps(messages)

You can also call these methods with different logging levels. While the default logging
level is ``error``, the following example outputs all ``info``, ``warning``, and ``error`` levels
to the logger when the script runs:

.. code-block:: python

    wb.run_script_file("a_script_file_name", log_level="info")

Upload and download files
=========================

You can upload and download data files to and from the server using the ``upload_file()`` and ``download_file``
methods. The client-side working directory is used to hold these files unless absolute paths or target directories
are specified. There is also a working directory on the server for the same purpose. To obtain the server’s working
directory, you can use the ``GetServerWorkingDirectory()`` query in the scripts that run on the server.

This code uploads all part files of a given prefix and all AGDB files in the working directory, along with another file
outside of the working directory, from the client to the server:

.. code-block:: python

    wb.upload_file("model?.prt", "*.agdb", "/path/to/some/file")

This server-side Workbench script loads an uploaded geometry file from the server's working directory into a
newly created Workbench system:

.. code-block:: python

    wb.run_script_string(
        r"""import os
    work_dir = GetServerWorkingDirectory()
    geometry_file = os.path.join(work_dir, "two_pipes.agdb")
    template = GetTemplate(TemplateName="Static Structural", Solver="ANSYS")
    system = CreateSystemFromTemplate(Template=template, Name="Static Structural (ANSYS)")
    system.GetContainer(ComponentName="Geometry").SetFile(FilePath=geometry_file)
    """
    )

This server-side Workbench script copies a Mechanical solver output file to the server's working directory:

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

This client script downloads all files with ``.out`` extensions from the server's working directory:

.. code-block:: python

    wb.download_file("*.out")

There is a special client method to upload a data file from the Ansys
`example-data <https://github.com/ansys/example-data/raw/master/pyworkbench>`_ repository
directly to the Workbench server. You should specify the file path relative to the
``pyworkbench`` folder in the ``example-data`` repository:

.. code-block:: python

    client.upload_file_from_example_repo("pymechanical-integration/agdb/two_pipes.agdb")

All methods for uploading and downloading files display a progress bar by default. You can
turn off the progress bar with an optional argument:

.. code-block:: python

    wb.download_file("solve.out", show_progress=False)

Start other PyAnsys services for systems in a Workbench project
==================================================================

PyMechanical
------------

For any Mechanical system in the Workbench project, you can start and connect the
PyMechanical service from the same client machine. This code runs a server-side script
to create a mechanical system. It then starts the PyMechanical service for the system
and establishes a PyMechanical client.

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

This code starts the PyFluent service and client for a Fluent system created in Workbench.

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

This code starts the PySherlock service and client for a Sherlock system created in Workbench.

.. code-block:: python

    from ansys.sherlock.core import launcher as pysherlock

    sys_name = wb.run_script_string(
        r"""import json
    wb_script_result=json.dumps(GetTemplate(TemplateName="SherlockPre").CreateSystem().Name)
    """
    )
    server_port = wb.start_sherlock_server(system_name=sys_name)
    sherlock = pysherlock.connect_grpc_channel(port=server_port)
