from panda3d.core import QueuedConnectionManager
from panda3d.core import QueuedConnectionReader
from panda3d.core import ConnectionWriter
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.task import Task
from direct.task.TaskManagerGlobal import taskMgr
from direct.showbase.ShowBase import ShowBase

class Client:
    def __init__(self):

        self.port = 5555
        self.addr = "127.0.0.1"
        self.timeout = 3000

        self.connect_to_server()
        
    def connect_to_server(self):
        self.manager = QueuedConnectionManager()
        self.reader = QueuedConnectionReader(self.manager, 0)
        self.writer = ConnectionWriter(self.manager, 0)
        try:
            self.connection = self.manager.openTCPClientConnection(self.addr, self.port, self.timeout)
            # Listen for data sent from server
            taskMgr.add(self.handle_server_connection, "Poll the connection listener", -40)
            print ("Connected to server...")
            self.reader.addConnection(self.connection)
            taskMgr.add(self.send_server_message, "Send msg", -41)
        except: 
            print ("Server not connected...")
        
    def handle_server_connection(self, task_data):
        if self.reader.dataAvailable():
            datagram = PyDatagram()
            if self.reader.getData(datagram):
                self.handle_server_message(datagram)
        return Task.cont

    def send_server_message(self, task_data):
        new_datagram = PyDatagram()
        new_datagram.addString("Hi from client")
        self.writer.send(new_datagram, self.connection)

    def handle_server_message(self, message):
        iterator = PyDatagramIterator(message)
        print (iterator.getString())
