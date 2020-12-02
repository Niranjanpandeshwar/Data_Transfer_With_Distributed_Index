import socket		
import os
import time	 
import json
import traceback, sys 
import csv
#import pandas as pd

List_of_files = 'C:\\Internet_Protocols\\List_of_files'
csv_receivedlist = 'C:\\Internet_Protocols\\Received_list\\csv_receivedlist.csv'
peer_list = []

Port_RS = 23475
Host_RS = '192.168.0.161'

hostname = socket.gethostname()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip1 = (s.getsockname()[0])
print(hostname)
portnumber = 10000

# Create a socket object
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)		  
#s.connect((Host_RS,Port_RS ))

class peerserver():
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port

def registration():
    x = 'Register_to_RS'
    message = json.dumps({"msg" : x , "Hostname" : hostname , "Portnumber" : str(portnumber)})
    s.send(message.encode())
    received_message = s.recv(2048).decode()
    print(received_message)
    recv_msg = json.loads(received_message)
    print(recv_msg["msg"])
    s.close()

def check_file(request):
    r = []
    for file in request.split(","):
            if file not in peer_list:
                file = file.strip()
                r.append(file)
                #print(r)
    return r

def requesting_peerlist():
    file_request = input("Enter the file to be requested: ")
    file = check_file(file_request)
    x = 'Active_peer'
    message = json.dumps({"msg" : x , "Hostname" : hostname , "Portnumber" : str(portnumber)})
    s.send(message.encode())
    received_message = s.recv(2048).decode()
    #print(received_message)
    recv_message = received_message.split('\n')
    #print(type(recv_message), len(recv_message), recv_message)
    if len(recv_message) == 1:
        print("No peers active")
        s.close()
    else:
        new_msg = recv_message[1]
        #print(type(new_msg))
        new_msg = new_msg.strip('[').strip(']').replace('}, {', '}!{').split('!')
        res = []
        for item in new_msg:
            res.append(json.loads(item))
        #print(res)
        for element in res:
            peer = peerserver(**element)
            print(peer)
            try:
                if(requesting_files(peer, file)):
                    break
            except Exception:
                traceback.print_exc(sys.stdout)
        if(len(res) != 0):
            print("All files received or No active peer left to check")
    s.close()
    
def checking_list(msg):
    #print("message", msg)
    f = open(csv_receivedlist)
    csv_f = csv.reader(f)
    attendee_emails = []
    for row in csv_f:

        d = row[0].split(";")
        attendee_emails.append(d)

    for i in msg:
        #b = i[0]
        c = i[0].split(";")

        if c in attendee_emails:
            pass
        else:
            count = 0
            for j in attendee_emails:
                if c[0] == j[0] and c[1] == j[1] and c[2] == j[2]:
                    #print("in loop")
                    ind = attendee_emails.index(j)
                    attendee_emails[ind] = c
                    count +=1
                    
            if count == 0:
                attendee_emails.append(c)
                #list1.append(c)
    
    for i in attendee_emails:
        print(';'.join(i))         
    
    with open(csv_receivedlist, 'w') as csvfile:
       spamwriter = csv.writer(csvfile)
       for i in attendee_emails:
           item = str(';'.join(i))
           spamwriter.writerow([item])
        

def requesting_files(peer: peerserver, file):
    #print(file)
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(peer.port)
    ip = peer.ip
    try:
        s1.connect((ip, port)) 
    except (ConnectionRefusedError , OSError, Exception) as e:
        # traceback.print_exc(sys.stdout)
        print("Couldnot connect to host: " + ip + ":" + str(port))
        return False
    #s1.connect((ip, port))
    x = 'listoffiles'
    message = json.dumps({"msg" : x , "Hostname" : hostname , "Portnumber" : str(portnumber)})
    s1.send(message.encode())
    received_message = s1.recv(2048).decode()
    #print(received_message)
    recv_message = received_message.split('\n')
    #print(type(recv_message), len(recv_message), recv_message)
    new_msg = recv_message[2]
    #print(new_msg) 
    r_msg = json.loads(new_msg)
    #print(r_msg)
    res_msg = checking_list(r_msg)
    #print("-------------------------------------------")
    print(res_msg)
    #print("-------------------------------------------")        
    if new_msg == '[]':
        res = 0
    else:
        #print("Im here")
        res = json.loads(new_msg)
        #print(res)
        for element in res:
            IPList = element[0].split(';')
            texttype = IPList[0].split('.')[0]
            ip_1 = IPList[1]
            port_1 = IPList[2]
            #print(texttype)
            for i in file:
                if texttype == i:
                    try:
                        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s2.connect((ip_1,int(port_1)))
                        x = 'Requesting_files'
                        message = json.dumps({"msg" : x ,"file" : i, "Hostname" : hostname , "Portnumber" : str(portnumber)})
                        #print(message)
                        s2.send(message.encode())
                        flag = '1'
                        reg_file_in_csv(i, ip1, portnumber, flag)
                        #print("Im")
                        recv_file(i, s2)
                    except Exception:
                        traceback.print_exc(sys.stdout)
                    finally:
                        s2.close()
    s1.close()
    return False

def recv_file(file, s):
    completeName = os.path.join(List_of_files, str(file) + ".txt")
    with open(completeName, 'wb') as file:
        while True:
            data = s.recv(2048)
            if not data:
                break
            file.write(data)
    file.close()
    global len_of_file
    len_of_file = (os.stat(completeName).st_size)*8
    #print(len_of_file)

def reg_file_in_csv(file, ip: str, port: str, flag):
    with open(csv_receivedlist, mode='a', newline ='') as myfile:
        wr = csv.writer(myfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        wr.writerow([str(file) +'.txt;' + ip + ';' + str(port) + ';' + flag])

def leave_message():
    x = 'Leave_the_server'
    message = json.dumps({"msg" : x , "Hostname" : hostname , "Portnumber" : str(portnumber)})
    s.send(message.encode())
    received_message = s.recv(2048).decode()
    #recv_msg = json.loads(received_message)
    print(received_message)
    s.close()
    
def peer_list_files():
    global exisiting_files
    for root, dirs, files in os.walk(List_of_files):
        #print(files)
        for file in files:
            if '.txt' in file:
                peer_list.append(file.split(".")[0])

peer_list_files()

choice = None
while True:
    print("1. Registering with RS\n2. Requesting Peer List and Files\n3. Leave the network")
    choice = int(input("Enter your request: "))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((Host_RS,Port_RS))
    if choice == 1:
        registration()
    elif choice == 2:
        start = time.time()
        requesting_peerlist()
        stop = time.time()
        time_diff = (stop - start)
        print("Total time taken:", str(stop - start))
        print("Throughput:", len_of_file/time_diff, "bps")
    else:
        leave_message()
        
        