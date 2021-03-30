import socket
import ipaddress
import sys

# assume these are both None as a return type these are just for readability
class Message: ...
class Connection: ...

class ClientSocketServer:

    def __init__(self, ip, port=5000):
        self.port = port
        self.ip = ip
        # Create a fully routable TCP_SOCKET -> man socket
        self.sok = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    # We implement ipaddress to validate ip_addresses
    def verify_ip_address(self) -> bool:

        try:
            # try to create a ip_address instance
            ip = ipaddress.ip_address(self.ip)

            if isinstance(ip, ipaddress.Ipv4Address):
                # return the ip_address instance
                return True

        except ValueError:
            print("Enter a valid IP Address")
            # we just want to exit here because the user did something wrong
            sys.exit(1)


    # the ability to connect to a MessageServer -> server.py
    def connect(self) -> Connection:

        # verify & give back a ipaddress
        #ip = ClientSocketServer.verify_ip_address(self.ip)

        # we cannot assume that this is going to be a ipaddress
        #if ip:
        self.sok.connect((self.ip, self.port))


        #else:
            # shutdown one or both halves of the connection.
            # further sends are disallowed.
        #self.sok.shutdown(socket.SHUT_RD)
        #self.sok.close()
        #print("\n")


    # send message to the MessageServer
    def send(self, message: Message) -> Message:
        sent = 0
        self.sok.sendall(message)

    # close both sides of the socket
    def close(self) -> None:
        #@self.sok.shutdown(socket.SHUT_RD)
        self.sok.close()


    # this is waiting for us to recv messages from our MessageServer
    # this will also act as our recv
    def wait_for_message(self) -> None: ...
        # to be impl'd

def main():
    if len(sys.argv) >= 2:
        print("Blank Line to write to a stdin")
        name = input("\nusername: ")
        client = ClientSocketServer(sys.argv[1])
        # this would allow us to reconnect not recursively
        while True: # this is really jaank
          client.connect() # no msg because this does not connect rip
          try:
              while True:
                  print("") # stamp buffer
                  next_message = input("") # this is blocking, only because of a syscall
                  # shadow next_message to include name
                  next_message = f'\n{name}: {next_message}'
                  client.send(bytes(next_message, 'utf-8'))
                  next_message = None
          except KeyboardInterrupt:
            client.close()
          except ConnectionResetError:
            continue
        sys.exit(0)
    else:
        print("Enter a valid IP Address\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
