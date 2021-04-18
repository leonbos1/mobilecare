import socket
import sqlite3
from datetime import datetime
import time
import db_commands as db
import requests

def main():
    HOST = "192.168.178.69" 
    PORT = 4000       
    first = False
    last_data = False
    sensor_id = 0
    previous_data = False
    first_end = False
    url = 'http://127.0.0.1:5000/sensordata/'


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        print("Binding done, waiting for client")
        s.listen()
        connection, addr = s.accept()
        
        with connection:
            print("Connected by", addr)
            while True:
                #resetting variables
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
                        activation_duration = round(endtime - starttime)-4 #-4 door afwijking door dubbele no_contact meting
                        end = datetime.now()
                        enddatetime_string = end.strftime("%d/%m/%Y %H:%M:%S")
                        data = {'sensor_id':sensor_id, 'time_activated':datetime_string, 'time_deactivated':enddatetime_string, 'tag':tag, 'activation_duration':activation_duration}
                        response = requests.put(url, data)
                        print(f'{sensor_id, datetime_string,enddatetime_string,tag, activation_duration} saved to database')
                        last_data = False
                    first_end = False

if __name__ == '__main__':
    main()