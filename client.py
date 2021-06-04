import socket
import time
import sys

HEADER = 64
PORT = 4000
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = "192.168.178.69"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_lenght = len(message)
    send_lenght = str(msg_lenght).encode(FORMAT)
    send_lenght += b' ' * (HEADER - len(send_lenght))
    client.send(send_lenght)
    client.send(message)

send("ALARM!")

alarm_on = False

def thread_function():
    while alarm_on:
        print("BEEP BEEP BEEP")
        time.sleep(1)

mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    mysock.bind(("",1234))
except:
    print("Fail to bind")
    sys.exit()

thrd = None
mysock.listen(5)
while True:
    conn, addr = mysock.accept()
    while True:
        conn, addr = mysock.accept()
        data = conn.recv(4000)
        state = b"ALARM ON":
        print(data)
        if not data:
            break
        if data == b"ALARM ON":
            state = b"ALARM ON"
            print(state)
            alarm_on = True

            thrd = threading.Thread(target=thread_function)
            thrd.start()
        if data == b"SILENT":
            state = b"ALARM OFF"
            print(state)

            alarm_on = False
        conn.sendall(state)
    conn.close()
mysock.close()


while True:
    data = client.recv(4000)
    print(data.decode("utf-8"))

    client.send(input(":::").encode("utf-8"))


