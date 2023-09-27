Start server
============
## Start Workbench server on local or remote computer
On a computer with standard ANSYS installation:
1. Start Workbench
2. In the Workbench Command Window, type `StartServer()`
3. Take a note of the returned port number that will be needed when starting a PyWorkbench client

By default, server's working directory uses the user preference for temporary
project file directory. One can also specify a different working directory:
`StartServer(WorkingDirectory="/path/to/a/writable/dir")`


Another way to start Workbench server, along with a connected client, is to use [PyWorkbench API](api/index).
