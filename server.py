import socket

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
                tag = ''
                scanner = ''
                scanner_bool = False
                tag_bool = True

                data = connection.recv(1024)
                message = data.decode("utf-8")
                if not data:
                    return
                print("Received data: ", message)
                for element in message:
                    if tag_bool:
                        tag += element
                        if element == ' ':
                            scanner_bool = True
                            tag_bool = False
                            
                    if scanner_bool:
                        scanner += element
                scanner= scanner[1:]


                print(tag)
                print(scanner)

if __name__ == '__main__':
    main()