import socket
import threading

server = "127.0.0.1"
port = 5555
clients = dict()
addresses = dict()

# New server socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind
try:
    sock.bind((server, port))
except socket.error as e:
    str(e)

# Listen
sock.listen(7)
print("Server listening...")

# Accept new connections
def accept_new_connections(socket: socket) -> None:
    """ Handle incoming clients """
    while True:
        client, client_addr = socket.accept()
        print("Connected to: {}".format(client_addr))
        client.send("Testing connection".encode("utf-8"))
        addresses[client] = client_addr
        threading.Thread(target=serve_client, args=(
            client, client_addr)).start()

# Receive and send data from single client
def serve_client(conn: str, addr: str) -> None:
    """ Serve client connection """
    name = conn.recv(2048).decode("utf-8")
    broadcast_msg = "%s has joined the room!" % name
    broadcast(broadcast_msg, name)
    clients[conn] = name
    # If conn.recv returns an empty bytes obj, the client has closed the connection

# Send message to all the clients for multiclient connections 
def broadcast(message: str, prefix: str) -> None:
    for client in clients:
        print(client)


def main():
    # New thread to wait for connections
    new_connections_thread = threading.Thread(
        target=accept_new_connections, args=(sock,))
    new_connections_thread.start()


if __name__ == "__main__":
    main()
