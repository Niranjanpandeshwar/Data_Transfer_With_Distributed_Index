import socket
import os
from _thread import *
import threading
import json
import csv
import datetime

file_name = []
file_list = []
file_location = 'C:\\Internet_Protocols\\List_of_files'
file_location.strip()
filepath_loc = 'C:\\Internet_Protocols\\Received_list\\csv_receivedlist.csv'
filepath = 'C:\\Internet_Protocols\\Received_list\\csv_receivedlist.csv'
path = 'C:\\Internet_Protocols\\List_of_files'
  
class peerthread(threading.Thread):
    
    def __init__(self,socket,client_ip):
        threading.Thread.__init__(self)
        self.lock=threading.Lock()
        self.csocket=socket
        self.ip=client_ip[0]
        self.socket=client_ip[1]

    def run(self):
        print("Received client connection from:" + threading.currentThread().getName())
        recmsg = self.csocket.recv(2048).decode('utf-8')
        print("Client's message: ", recmsg)
        req = json.loads(recmsg)
        #print(req)
        Message_type, Hostname, Portnumber = req["msg"], req["Hostname"], req["Portnumber"]

        if Message_type == 'Requesting_files':
            filename = req["file"]
            #print(filename)
            filename = filename.strip()
            #print(filename)
            file1 = filename + '.txt'
            #print(file1)
            file_path = file_location + '\\'+ file1
            if file1 in file_name:
                fileSize = os.stat(file_path).st_size
                try:
                    f = open (file_path,'rb')  
                except:
                    print("Error: Unable to open the file: %s",file_path)
                    errmsg = "404: Not Found"
                    self.csocket.send(errmsg.encode('utf-8'))
                    self.csocket.close()
                    exit()

                x = f.read(2048)
                while (fileSize > 0):
                    self.csocket.send(x)
                    fileSize -= 2048
                    #print(fileSize)
                    x = f.read(2048)
                    if((fileSize == 0) or (fileSize<0)):
                        f.close()
                        break
                print("File Sent: %s",file_path)
                self.csocket.close()

            else:
                print("Error: File Not Found: ",file_path)
                errmsg = "404: Not Found"
                self.csocket.send(errmsg.encode('utf-8'))
                self.csocket.close()
                exit()
                

        elif Message_type == 'listoffiles':
            global filepath_loc
            list_of_files = []
            with open(filepath_loc, 'r') as fil:
                read = csv.reader(fil)
                #print("Read", read)
                for record in read:
                    list_of_files.append(record)
            data = json.dumps(list_of_files)
            #print("Data", data)
            response = 'Successful' + '\n' + str(datetime.datetime.now()) + '\n' + data
            #print(response)
            self.csocket.send(response.encode())
            print("Data Sent")

def extracting_files(path):
    global filepath
    path1 = path
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = (s.getsockname()[0])
    #print(ip)
    s.close()
    port1 = str(port)
    for list1 in os.listdir(path1):
        if os.path.isfile(os.path.join(path1, list1)):
            fileName = list1 + ';' + ip + ';' + port1 + ';' + '1'
            file_list.append(fileName)
    #print(file_list)
    print("Storing the files present in the local Server to: ",filepath)
    with open(filepath,'w', newline ='') as f:
        writer = csv.writer(f)
        for word in file_list:
            writer.writerow([word])
     
def extracting_file_names(path):
    path1 = path
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    port1 = str(port)
    for list1 in os.listdir(path1):
        if os.path.isfile(os.path.join(path1, list1)):
            #print(list1)
            file_name.append(list1)
    #print(file_name)

thread_list = []
port = 10000
def main():
    global path
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("All the files in the present working directory:")
    extracting_files(file_location)
    extracting_file_names(file_location)
    Host = ''
    s.bind((Host,port))
    print ("socket binded to %s " %(port))

    while True:
        s.listen(6)
        print('The Server Socket is listening')
        client_conn, client_ip= s.accept()
        th = peerthread(client_conn,client_ip)
        th.start()
        thread_list.append(th) 
    
for i in thread_list:
	i.join()

main()