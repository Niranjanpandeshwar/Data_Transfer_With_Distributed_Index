TCP Protocol:

Files Required: Server.py, client.py, registrationserver.py, csvfile.py

A - Environment Settings
Required -
Windows machine
Python Version>=3

Registration Server
The registration server has to be run on a separate system as it acts as Registration Server and has the database of all the active peers in the network. The modules required for registrationserver.py are 
socket, json. To execute, just run the file from command line when all the modules are satisfied. In the script we have to change the port number to our wish (Currently the port number is server_port = 23475). There are no limitations hence the port number can be anything from 1 to 65535. The file would run and wait for connections, the messages are shown accordingly in the terminal.
command to run this file : python registrationserver.py

Peers
Both Server.py and client.py can be run the same system.

Server
The modules required to run this file are socket, os, threading, csv, json and datetime. We have to create an empty csv file in the given file path. We need to have txt files downloaded in the same file location as csv where the script is executed. Server code listens at a specified port and send all the requested files to the client.

Steps to run Server.py
1) Enter the port number of the server as your wish but it has to match with the port number of client if you are running on the same system.
2) Specify the path of csv file (For example - 'C:\\Internet_Protocols\\Received_list\\csv_receivedlist.csv') [This is the path where csv exist, userdefined in the code] in the script, similarly specify the path of the downloaded text files ('C:\\Internet_Protocols\\List_of_files') [This is the path where text files exist, userdefined in the code]
4) command to run this file : python Server.py

Client 
The modules required to run this file are socket, os, time, json, traceback, sys and csv.  Follow the same steps as in while executing the Server.py file. Client file registers the peers to the registration server and fetches all the files required from all the other peers when requested.

Steps to run the client.py
1) Enter the port number and the IP address of the Registration server in the script.
2) Specify the path of both csv and list of files downloaded in the script as done in server code.
3) Execute the script in command line
4) command to run this file : python client.py

csvfile.py
This script helps in updating the list of files present in their system every 30 seconds. So if there is any deletion of file in one peer it updates the csv file with the value of '0' in the flag bit.
command to run this file : python csvfile.py

Procedure to execute Server.py and client.py in the same system

1) Run the csvfile.py in the command line
2) Execute the registerationserver.py as explained
3) Run the client.py file and register to the Registration server
4) Run server on the same port as specified in client code

C - Interpretation of Results

Once you execute the client.py using the above mentioned command, the following input are to be entered:

Inputs

1. Registering with RS - Peer registers to the Registration Server (RS)
2. Requesting Peer List and Files - Receives list of files and the file requested
3. Leave the network - Peer exits the RS

On successful execution the requested file will be present in the destination path specified.



Along with the code and report we are attaching text files and csv file.





