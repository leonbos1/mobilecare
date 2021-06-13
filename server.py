import socket
import _thread
from datetime import datetime
import time
import requests
import json

def main():  #door leon
    HOST = "192.168.178.69" 
    PORT = 4000  
    threadcount = 0 
    
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

def threaded_client(connection):
    first = True
    last_data = False
    sensor_id = 0
    first_end = False
    url = 'http://127.0.0.1:5000/sensordata'
    while True:
        #receiving data 
        data = connection.recv(1024)
        message = data.decode("utf-8")
        print("Received data: ", message)
        json_data = json.loads(message)
        no_contact = json_data['no_contact']
        
        #converting received string to variables
        if no_contact == False:
            tag = json_data['tag']
            sensor_id = json_data['scanner']

            if first:
                first = False
                starttime = time.time()
                now = datetime.now()
                datetime_string = now.strftime("%d/%m/%Y %H:%M:%S")

            last_data = True
            first_end = True
            endtime = time.time()
            activation_duration = round(endtime - starttime)
            if activation_duration > 1800:
                endtime = time.time()
                end = datetime.now()
                enddatetime_string = end.strftime("%d/%m/%Y %H:%M:%S")
                data = {'sensor_id':sensor_id, 'time_activated':datetime_string, 'time_deactivated':enddatetime_string, 'tag':tag, 'activation_duration':activation_duration}
                response = requests.put(url, data)
                if response.status_code == 201:
                    print(f'{sensor_id, datetime_string,enddatetime_string,tag, activation_duration} saved to database')
                    starttime = time.time()
                else:
                    print("Failed to save data to database")
                

        else:
            if last_data and not first_end:
                first = True
                endtime = time.time()
                activation_duration = round(endtime - starttime)
                end = datetime.now()
                enddatetime_string = end.strftime("%d/%m/%Y %H:%M:%S")
                data = {'sensor_id':sensor_id, 'time_activated':datetime_string, 'time_deactivated':enddatetime_string, 'tag':tag, 'activation_duration':activation_duration}
                response = requests.put(url, data)
                if response.status_code == 201:
                    print(f'{sensor_id, datetime_string,enddatetime_string,tag, activation_duration} saved to database')
                else:
                    print("Failed to save data to database")
                last_data = False
            first_end = False
            
    connection.close()

if __name__ == '__main__':
    main()