import socket
import sqlite3
from datetime import datetime
import time
import db_commands as db

def main():
    HOST = "192.168.178.69" 
    PORT = 4000       
    first = False
    last_data = False
    sensor_id = 0
    previous_data = False

    conn = sqlite3.connect('sensor.db', check_same_thread=False)
    c = conn.cursor()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        print("Binding done, waiting for client")
        s.listen()
        connection, addr = s.accept()
        
        with connection:
            print("Connected by", addr)
            while True:
                #resetting variables
                tag = ''
                scanner = ''
                scanner_bool = False
                tag_bool = True
                
                
                #receiving data 
                data = connection.recv(1024)
                message = data.decode("utf-8")
                print("Received data: ", message)

                #converting received string to variables
                for element in message:
                    if tag_bool:
                        tag += element
                        if element == ' ':
                            scanner_bool = True
                            tag_bool = False
                    if scanner_bool:
                        scanner += element
                        if not previous_data:
                            first = True
                        previous_data = True
                        last_data = True
                print(scanner)
                if '1' in scanner:
                    sensor_id = 1
                elif '2' in scanner:
                    sensor_id = 2
                        
                if first:
                    nowtime = time.time()
                    now = datetime.now()
                    datetime_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    first = False

                if scanner == '':
                    previous_data = False
                    if last_data:
                        end = datetime.now()
                        enddatetime_string = end.strftime("%d/%m/%Y %H:%M:%S")
                        db.addtosensordata(sensor_id, datetime_string, enddatetime_string)
                        last_data = False

if __name__ == '__main__':
    main()