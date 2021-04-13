import socket
import time
import sqlite3
import keyboard


def main():
    HOST = "192.168.178.69" 
    PORT = 4000       
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        print("Binding done, waiting for client")
        s.listen()
        connection, addr = s.accept()
        
        with connection:
            print("Connected by", addr)
            while True:
                data = connection.recv(1024)
                message = data.decode("utf-8")
                if not data:
                    return
                print("Received data: ", message)

if __name__ == '__main__':
    main()