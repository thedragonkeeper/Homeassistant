import socket, ssl
import threading
from commands import Commands
import time
import json

def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper


class Client(object):
    def __init__(self, server, port, cert):
        self.port = port
        self.host = server
        self.connected = False
        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        self.context.load_verify_locations(cafile=cert)
        self.devices = {}
        self.commands = Commands(self)

    def ConnectToServer(self):
        self.DisconnectFromServer()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.connection = self.context.wrap_socket(self.sock,server_hostname=str(self.host))
        self.connected = True
        self.RecieveData()

    def DisconnectFromServer(self):
        self.connected = False
        try:
            self.connection.close()
        except:
            pass

    @threaded
    def RecieveData(self):
        while self.connected == True:
            data = self.connection.recv(1024)
            if data:
                self.handle_data_in(data.decode())
            else:
                self.DisconnectFromServer()


    def senddata(self, message):
        self.connection.sendall(bytes(message, encoding='utf-8'))

    def handle_data_in(self, data):
        #print(data)
        if "{" in data and "}" in data:
            request = json.loads(data)
            self.commands.client_in(request)
