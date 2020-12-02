from tempfile import NamedTemporaryFile
import shutil
import csv
import socket
import os
import time

filepath = 'C:\\IP\\RFCS\\'
filename = 'C:\\IP\\ips.csv'
csv_receivedlist = "C:\\IP\\ips.csv"        # It will generate on its own, no need to create a csv file

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP = (s.getsockname()[0])
print(IP)
s.close()

e = time.time() + 60*60
while time.time()<e:
    
    #port1 = str(port)
    list_of_files = []
    for entry in os.listdir(filepath):
        if os.path.isfile(os.path.join(filepath, entry)):
            #print ("asdfasdf")
            #print(entry)
            list_of_files.append(entry)
    print(list_of_files)

    tempfile = NamedTemporaryFile(mode='w', delete=False)

    with open(filename, 'rt') as csvfile, tempfile:
        reader = csv.reader(csvfile, delimiter=';')
        #writer = csv.DictWriter(tempfile, fieldnames=fields)
        for row in reader:
            #print("now")
            #print(row)
            if row[1] == IP:
                if row[0] in list_of_files:
                    row[3] = '1'
                else:
                    row[3] = '0'

            print(row)
            with open(csv_receivedlist, mode='a', newline ='') as myfile:
                wr = csv.writer(myfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                wr.writerow([row[0] + ';' + row[1] + ';' + row[2] + ';' + row[3]])
            

    shutil.move(csv_receivedlist, filename)
    time.sleep(5)