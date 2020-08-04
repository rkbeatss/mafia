from panda3d.core import QueuedConnectionManager
from panda3d.core import QueuedConnectionListener
from panda3d.core import QueuedConnectionReader
from panda3d.core import ConnectionWriter
from panda3d.core import PointerToConnection
from panda3d.core import NetAddress
from panda3d.core import NetDatagram
from direct.task import Task
from direct.task.TaskManagerGlobal import taskMgr
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator


class Server:
    def __init__(self):

        self.port = 5555
        self.addr = "127.0.0.1"
        self.backlog = 7
        self.active_connections = dict()
        self.start = False

        self.connect()

    def connect(self) -> None:
        # Handle connections and terminations
        self.manager = QueuedConnectionManager()
        # Wait for clients connection requests
        self.listener = QueuedConnectionListener(self.manager, 0)
        # Buffers incoming data from active connection
        self.reader = QueuedConnectionReader(self.manager, 0)
        # Transmit PyDatagrams to active connection
        self.writer = ConnectionWriter(self.manager, 0)
        # Open TCP Rendezvous to accept client connections with a limit
        self.socket = self.manager.openTCPServerRendezvous(
            self.port, self.backlog)
        self.listener.addConnection(self.socket)
        print("Server listening on port %s...." % str(self.port))
        # Listen for mew incoming connections
        taskMgr.add(self.handle_incoming_connections,
                    "Poll the connection listener", -39)
        # Listen for new datagrams
        taskMgr.add(self.handle_connection_data,
                    "Poll the connection reader", -40)
        # Listen for dropped connections
        taskMgr.add(self.handle_dropped_connections,
                    "Poll the dropped connection listener", -41)
        # See if game can be started
        taskMgr.add(self.start_game, "Start Game", -42)

    def start_game(self, task_data: Task) -> Task:
        if len(self.active_connections) == self.backlog:
            self.start = True
        return Task.cont

    def handle_incoming_connections(self, task_data: Task) -> Task:
        if self.listener.newConnectionAvailable():
            rendezvous = PointerToConnection()
            net_addr = NetAddress()
            new_connection = PointerToConnection()
            if self.listener.getNewConnection(rendezvous, net_addr, new_connection):
                new_connection = new_connection.p()
                # Keep track of our active connections
                self.active_connections[str(
                    new_connection.this)] = new_connection
                # Start reading the new connection
                self.reader.addConnection(new_connection)
                print("%s just connected" % str(new_connection))
        return Task.cont

    def handle_connection_data(self, task_data: Task) -> Task:
        if self.reader.dataAvailable():
            # Catch the incoming data
            datagram = NetDatagram()
            if self.reader.getData(datagram):
                name = self.handle_client_message(datagram)
                broadcast = f"Everyone, welcome {name} to the game!"
                self.broadcast_message(broadcast)

        return Task.cont

    def handle_dropped_connections(self, task_data: Task) -> Task:
        if self.manager.resetConnectionAvailable():
            connection_pointer = PointerToConnection()
            self.manager.getResetConnection(connection_pointer)
            lost_connection = connection_pointer.p()
            print("% s disconnected from server" % str(lost_connection))
            del self.active_connections[str(lost_connection.this)]
            self.manager.closeConnection(lost_connection)
        return Task.cont

    def handle_client_message(self, message: str) -> str:
        iterator = PyDatagramIterator(message)
        return iterator.getString()

    def get_connections_count(self) -> int:
        return len(self.active_connections)

    def send_personal_message(self, message: str, client: PointerToConnection) -> None:
        datagram = self.create_new_datagram(message)
        self.writer.send(datagram, client)

    def broadcast_message(self, message: str) -> None:
        datagram = self.create_new_datagram(message)
        for client in self.active_connections:
            self.writer.send(datagram, self.active_connections[client])

    def create_new_datagram(self, message: str) -> PyDatagram:
        new_datagram = PyDatagram()
        new_datagram.addString(message)
        return new_datagram

    def terminate_all_clients(self) -> None:
        for client in self.active_connections:
            self.reader.removeConnection(client)
        self.active_connections = list()

    def terminate_specific_client(self, client: PointerToConnection) -> None:
        self.reader.removeConnection(client)
        del self.active_connections[str(client)]
