import socket
import threading

class Client:
    def __init__(self):
        # New client socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 5555
        self.addr = (self.server, self.port)
        # Initialize a three way handshake to connect to server
        self.connection = self.connect()

    def get_connection(self) -> bool:
        return self.connection 

    def connect(self) -> None:
        try:
            self.client.connect(self.addr)
            self.client.sendall(b'Rupsi')
            # New thread to receive data 
            receive = threading.Thread(target = receive, args = (self.client, True))
            receive.start()
        except:
            print("Could not connect to server...")

    def send(self, data) -> None:
        try: 
            self.client.send(str.encode(data))
        except socket.error as e:
            print(e)

    def receive(self, socket: socket, connection: bool) -> None:
        while connection:
            try:
                data = socket.recv(32)
                print(str(data.decode("utf-8")))
            except:
                print("Disconnected from the server...")
                connection = False 
                break 
        
Client()