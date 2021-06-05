import socket
import _thread
from datetime import datetime
import time
import requests

def main():  #door leon
    HOST = "192.168.178.69" 
    PORT = 4000  
    threadcount = 0 
    client_tag = 'DSFGHERH'  
    
    serversocket = socket.socket()
    try:
        serversocket.bind((HOST,PORT))
    except socket.error as e:
        print(str(e))
    
    print("Waiting for connections")
    serversocket.listen(5)
    while True:
        Client, address = serversocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        _thread.start_new_thread(threaded_client, (Client, ))
        threadcount += 1
        print('Thread Number: ' + str(threadcount))
    serversocket.close()            

def threaded_client(connection): #door leon
    first = True
    last_data = False
    sensor_id = 0
    previous_data = False
    first_end = False
    url = 'http://192.168.178.69:80/sensordata'
    while True:
        scanner = ''
        scanner_bool = False
        tag_bool = True
        #receiving data 
        data = connection.recv(1024)
        message = data.decode("utf-8")
        print("Received data: ", message)
        #converting received string to variables
        if 'no_contact' not in message:
            tag = ''
            for element in message:
                if tag_bool:
                    tag += element
                    if element == ' ':
                        scanner_bool = True
                        tag_bool = False
                if scanner_bool:
                    scanner += element
                    first_end = True
                    if not previous_data:
                        first = True
                    previous_data = True
                    last_data = True
        
        if '1' in scanner:
            sensor_id = 1
        elif '2' in scanner:
            sensor_id = 2
        elif '3' in scanner:
            sensor_id = 3
        elif '4' in scanner:
            sensor_id = 4
                
        if first:
            starttime = time.time()
            nowtime = time.time()
            now = datetime.now()
            datetime_string = now.strftime("%d/%m/%Y %H:%M:%S")
            first = False

        if scanner == '':
            previous_data = False
            if last_data and not first_end:
                endtime = time.time()
                activation_duration = round(endtime - starttime)
                end = datetime.now()
                enddatetime_string = end.strftime("%d/%m/%Y %H:%M:%S")
                data = {'sensor_id':sensor_id, 'time_activated':datetime_string, 'time_deactivated':enddatetime_string, 'tag':tag, 'activation_duration':activation_duration}
                response = requests.put(url, data)
                print(f'{sensor_id, datetime_string,enddatetime_string,tag, activation_duration} saved to database')
                last_data = False
            first_end = False
    connection.close()

if __name__ == '__main__':
    main()