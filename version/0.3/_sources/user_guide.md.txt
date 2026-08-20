# User guide
This section provides an overview of the PyWorkbench package, explaining
key concepts and approaches when working with Workbench gRPC service.


## Start Workbench client and connect to a running Workbench server
A typical user of Workbench gRPC service starts a Workbench client that connects to
a running Workbench server on cloud, given the server's name/IP and port.
A client-side working directory should be specified. This directory is the default
location for client-side files.
```
from ansys.workbench.core.workbench_client import WorkbenchClient
workdir = "path_to_the_local_working_directory"
host = "server_machine_name_or_ip"
port = server_port_number
wb = WorkbenchClient(workdir, host, port)
wb.connect()
```

## Launch Workbench server and start a client
During development phase or for debugging purpose, it is useful to start Workbench server on the developer's desktop or some computer within the company network.

One can always start a Workbench server by executing command `StartServer()` in any running Workbench session and use the returned server port to start a client, like in the example above.

Alternatively, one can launch a Workbench server and start a client programmatically in client-side Python script. To launch a server on the local computer:
```
from ansys.workbench.core import launch_workbench
wb = launch_workbench()
```
or to launcher a server on a remote Windows machine with valid user credentials:
```
from ansys.workbench.core import launch_workbench
host = "server_machine_name_or_ip"
username = "your_username_on_server_machine"
password = "your_password_on_server_machine"
wb = launch_workbench(host=host, username=username, password=password)
```
There are other options to this `launch_workbench` API, such as specifying a certain Workbench release to launch, or to use particular working directories on the server and/or at the client instead of the default directories.
```
from ansys.workbench.core import launch_workbench
wb = launch_workbench(release='241', server_workdir='path_to_a_dir_on_server', client_workdir='path_to_a_dir_on_client')
```

## Run script/commands/queries on Workbench server
IronPython based Workbench scripts containing commands/queries can be executed on the server via
* `run_script_file`, which execute a script file in the client working directory; or
* `run_script_string`, which execute a script contained in the given string

Any output that needs to be returned from these APIs can be assigned to the global variable `wb_script_result` in the script as a JSON string. For example, the following Workbench script returns all message summaries from the Workbench session:
```
import json
messages = [m.Summary for m in GetMessages()]
wb_script_result = json.dumps(messages)
```
These run_script APIs can also be called with different logging levels. The default logging level is 'error'. The following line will output to the logger all info/warnings/errors during the script run.
```
wb.run_script_file('a_script_file_name', log_level='info')
```

## File handling
Data files can be uploaded to the server or downloaded from the server, using `upload_file` or `download_file` API. The client-side working directory is used to hold these files unless absolute paths or target directory is specified. There is also a working directory on the server for the same purpose. The server's working directory can be obtained via Workbench query `GetServerWorkingDirectory()` that runs on the server.

For example, this uploads all part files with a given prefix and all agdb files in the working directory, plus another file outside of the working directory, from client to server:
```
wb.upload_file('model?.prt', '*.agdb', '/path/to/some/file')
```

The following server side Workbench script loads an uploaded geometry file from the server's working directory into a newly created Workbench system:
```
wb.run_script_string(r'''import os
work_dir = GetServerWorkingDirectory()
geometry_file = os.path.join(work_dir, "2pipes.agdb")
template = GetTemplate(TemplateName="Static Structural", Solver="ANSYS")
system = CreateSystemFromTemplate(Template=template, Name="Static Structural (ANSYS)")
system.GetContainer(ComponentName="Geometry").SetFile(FilePath=geometry_file)
''')
```
The following server side Workbench script copies a Mechanical solver output file to the server's working directory to be downloaded later:
```
wb.run_script_string(r'''import os
import shutil
work_dir = GetServerWorkingDirectory()
mechanical_dir = mechanical.project_directory
out_file_src = os.path.join(mechanical_dir, "solve.out")
out_file_des = os.path.join(work_dir, "solve.out")
shutil.copyfile(out_file_src, out_file_des)
''')
```
This client script downloads all files with .out extension from the server's working directory:
```
wb.download_file('*.out')
```

There is a special client API to upload a data file from [the ANSYS example database](https://github.com/ansys/example-data/tree/master/pyworkbench) directly to the Workbench server. The file name and subdirectory name in the database should be specified:
```
client.upload_file_from_example_repo("2pipes.agdb", "2pipes")
```

All the file handling APIs come with progress bar that is shown by default. One can turn off progress bar with an optional argument:
```
wb.download_file('solve.out', show_progress=False)
```

## Start other PyANSYS services from systems in a PyWorkbench project
### PyMechanical
For any mechanical system in the Workbench project, PyMechanical service can be started and connected to from the same client machine.
The following runs a server side script to create a mechanical system, then starts PyMechanical service for the system and establish a PyMechanical client.
```
from ansys.mechanical.core import launch_mechanical
sys_name = wb.run_script_string(r'''import json
wb_script_result=json.dumps(GetTemplate(TemplateName="Static Structural (ANSYS)").CreateSystem().Name)
''')
server_port=wb.start_mechanical_server(system_name=sys_name)
mechanical = launch_mechanical(start_instance=False, ip='localhost', port=server_port)"
```
### PyFluent
This example illustrates how to start PyFluent service and client for a Fluent system created in Workbench.
```
import ansys.fluent.core as pyfluent
sys_name = wb.run_script_string(r'''import json
wb_script_result=json.dumps(GetTemplate(TemplateName="FLUENT").CreateSystem().Name)
''')
server_info_file=wb.start_fluent_server(system_name=sys_name)
fluent=pyfluent.connect_to_fluent(server_info_filepath=server_info_file)
```
