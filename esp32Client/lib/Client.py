import socket, ssl
from commands import Commands
import time
import json


class Client(object):
    def __init__(self, server, port, cert, config):
        self.port = port
        self.host = server
        self.cert = cert
        self.connected = False
        self.devices = {}
        self.commands = Commands(self, config)
      
    def ConnectToServer(self):
        self.DisconnectFromServer()
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            self.connection = ssl.wrap_socket(self.sock, server_hostname=str(self.host),  cert=self.cert)
            self.connected = True
            return 0
        except Exception as error:
            print("connect error "+str(error))
            if str(error) == "23":
                return 23
            else:
                return 1

    def DisconnectFromServer(self):
        self.connected = False
        try:
            self.connection.close()
        except:
            pass

    def RecieveData(self):
        data = self.connection.readline()
        if data:
            self.handle_data_in(data.decode())
        else:
            self.DisconnectFromServer()


    def senddata(self, message):
        self.connection.write(message)

    def handle_data_in(self, data):
        if "{" in data and "}" in data:
            request = json.loads(data)
            self.commands.client_in(request)
