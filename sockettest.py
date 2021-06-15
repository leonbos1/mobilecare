import socket
import _thread
import json

HOST = '127.0.0.1'
PORT = 4000
def main():
    while True:
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

                 
def threaded_client(connection):
    while True:
 
        data = connection.recv(1024)
        message = data.decode("utf-8")
        print("Received data: ", message)
        json_data = json.loads(message)
        print(f"patient is {json_data['patient_id']}")
        print(f"reason is {json_data['reason']}")

if __name__ == '__main__':
    main()