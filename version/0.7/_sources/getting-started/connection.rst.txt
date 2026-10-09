Connecting with Ansys Workbench
###############################

This guidelines describe step by step how to connect PyWorkbench to Ansys
Workbench. Different options exist, including local and remote connections.

Local connection
================

You can connect PyWorkbench to a local session of Ansys Workbench by running
the following steps:

1. Start Ansys Workbench
2. In the Workbench Command Window, type ``StartServer()``
3. Take a note of the returned port number
4. Use the port number to connect PyWorkbench to the server:

.. code-block:: python

    from ansys.workbench.core import connect_workbench

    workbench = connect_workbench(port=port)

Remote connection
=================
You can connect PyWorkbench to an Ansys Workbench session running on a remote
computer by giving its computer name or IP and the port number that the service uses:

.. code-block:: python

    from ansys.workbench.core import connect_workbench

    workbench = connect_workbench(host=host_name_or_IP, port=port)
