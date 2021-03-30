import socket
import ipaddress
import sys

class Connection: ...

class MessageServer:

    def __init__(self, port=5000):
        self.port = port
        self.host = '127.0.0.1'
        self.sok = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_server(self) -> Connection:
        self.sok.bind((self.host, self.port))
        self.sok.listen(2) # accept 2 incomming connections
        conne, address = self.sok.accept()
        with conne:
            print("\nwelcome\n")
            while True:
                try:
                    data = conne.recv(2048)
                    if data != b'':
                        print(str(data, 'utf-8'))
                        print("\n")
                    conne.sendall(data)
                except KeyboardInterrupt:
                    self.sok.close()
            self.sok.close()

    def close(self) -> None:
        self.sok.close()

def main():
    msgserver = MessageServer()
    msgserver.start_server()
    msgserver.close()
    sys.exit(0)

if __name__ == "__main__":
    main()

