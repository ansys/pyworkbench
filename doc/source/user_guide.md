# workig with Workbench gRPC service


## start Workbench client and connect to a running Workbench server
General users of Workbench gRPC service typically starts a Workbench client that connects to a running Workbench server on cloud, given the server's host name/IP and port.
A client side working directory should be specified. This directory is the default location for client side files.
```
from ansys.api.workbench.v0.workbench_client import WorkbenchClient
workdir = "path_to_the_local_working_directory"
host = "server_machine_name_or_ip"
port = server_port_number
wb = WorkbenchClient(workdir, host, port)
wb.connect()
```

## start Workbench server and client
For solution method developers, it is often useful for implementation or debugging purpose to start Workbench server on the developer's desktop or some computer within the company network. One can manually start a Workbench server by executing command `StartServer()` in any Workbench session and take a note of the returned server port.

Alternatively, one can launch Workbench server and client in Python script. To launch it on the local computer:
```
from ansys.api.workbench.v0.launch_workbench import LaunchWorkbench
wb = LaunchWorkbench()
```
or to launcher server on a remote Windows machine with valid user credentials:
```
from ansys.api.workbench.v0.launch_workbench import LaunchWorkbench
host = "server_machine_name_or_ip"
username = "your_username_on_server_machine"
password = "your_password_on_server_machine"
wb = LaunchWorkbench(host, username, password)
```
There are options to launch Workbench server of a certain release, or to use specified working directories on server or client side instead of the default directories.
```
from ansys.api.workbench.v0.launch_workbench import LaunchWorkbench
wb = LaunchWorkbench(release='241', server_workdir='path_to_a_dir_on_server', client_workdir='path_to_a_dir_on_client')
```

## run commands/queries on Workbench server
Workbench scripts containing commands/queries can be executed on the server via
* `run_script_file`, which execute a script file in the client working directory; or
* `run_script_string`, which execute a script contained in the given string

Any output that needs to be returned from these APIs can be assigned to the global variable `wb_script_result` in the Workbench script, as a JSON string. For example, the following Workbench script returns all message summaries from the Workbench session:
```
import json
messages = [m.Summary for m in GetMessages()]
wb_script_result = json.dumps(messages)
```
These run_script APIs can also be called with different logging levels. The default logging level is 'error'. The following line will print out all messages logged as either info/warning/error during the script run.
```
wb.run_script_file('a_script_file_name', log_level='info')
```

## file handling
Data files can be uploaded to the server or downloaded from the server, using `upload_file` or `download_file` API. The client-side working directory is used to hold these files. There is also a working directory on the server for the same purpose. The server's working directory can be obtained via Workbench query `GetServerWorkingDirectory()`.

This uploads all part files with a given prefix and all agdb files in the working directory, plus another file outside of the working directory, from client to server:
```
wb.upload_file('model?.prt', '*.agdb', '/path/to/some/file')
```

The following server side Workbench script loads an uploaded geometry file from the server's working directory into a newly created Workbench system:
```
import os
work_dir = GetServerWorkingDirectory()
geometry_file = os.path.join(work_dir, "2pipes.agdb")
template = GetTemplate(TemplateName="Static Structural", Solver="ANSYS")
system = CreateSystemFromTemplate(Template=template, Name="Static Structural (ANSYS)")
system.GetContainer(ComponentName="Geometry").SetFile(FilePath=geometry_file)
```
The following server side Workbench script copies a Mechanical solver output file to the server's working directory to be downloaded later:
```
import os
import shutil
work_dir = GetServerWorkingDirectory()
mechanical_dir = mechanical.project_directory
out_file_src = os.path.join(mechanical_dir, "solve.out")
out_file_des = os.path.join(work_dir, "solve.out")
shutil.copyfile(out_file_src, out_file_des)
```
The client can then download all output file from the server:
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

## start other PyANSYS services based on PyWorkbench
### PyMechanical
For any mechanical system in the Workbench project, PyMechanical service can be started and connected to from the same client machine.
The following server side script starts PyMechanical service for an existing Workbench system and returns the port used by the service.
```
import json
model = system.GetContainer(ComponentName="Model")
model.Edit()
mech_port = model.StartGrpcServer()
wb_script_result = json.dumps(mech_port)
```
The following client script launches a PyMechanical client based on the port returned, then print the mechanical service's project directory.
```
from ansys.mechanical.core import launch_mechanical
mechanical = launch_mechanical(start_instance=False, ip=host, port=mech_port)
print(mechanical.project_directory)
```
### PyFluent
to be implemented
