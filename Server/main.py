import socket, ssl
import threading
import time
from commands import Commands
from admincommands import adminCommands

###openssl req -x509 -newkey rsa:4096 -sha256 -days 3650 -nodes   -keyout my.key -out my.crt   -addext 'subjectAltName=IP:192.168.1.167'
##create keys command

def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper

class Server(object):
    def __init__(self, host, port, cert="", key="", admin=False, client_server=None):
        self.coms = Commands(self)
        self.clients = {}
        self.port = port
        self.host = host
        self.listening = False
        self.use_ssl = True
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain(certfile=cert, keyfile=key)
        self.admin = admin
        if admin == True:
            self.client_server = client_server
            self.adcoms = adminCommands(self)

    def StartServer(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        self.listening = True
        self.listen()

    def send_message(self, client, message):
        if "SSLSocket" == type(client).__name__:
            client.write(bytes(message, encoding='utf-8'))
        elif "str" == type(client).__name__:
            client = self.clients[str(client)]["connection"]
            client.write(bytes(message, encoding='utf-8'))

    @threaded
    def listen(self):
        while self.listening == True:
            if self.admin == True:
                print("waiting on admins . . .")
            else:
                print("waiting on clients . . .")
            connection, client_addr = self.sock.accept()
            try:
                if self.use_ssl == True:
                    connection = self.context.wrap_socket(connection, server_side=True)

                id = 1
                while True:
                    if str(id) not in self.clients:
                        self.clients[str(id)] = {
                            "id": id,
                            "connection": connection,
                            "addr": client_addr,
                            "data": {}
                            }
                        break
                    id += 1
                if self.admin == True:
                    print("admin connected: "+str(client_addr)+" as id: "+str(id))
                    self.admin_client(str(id), connection)
                else:
                    print("client connected: "+str(client_addr)+" as id: "+str(id))
                    self.client(str(id), connection)
            except:
                print("error connection may have closed before wrap")

    def close_client(self, id):
        if id in self.clients.keys():
            try:
                self.clients[id]["connection"].close()
            except:
                pass
            self.clients.pop(str(id))
            if self.admin == True:
                print("admin disconnected: "+str(id))
            else:
                print("client disconnected: "+str(id))

    @threaded
    def client(self, id, connection):
        while self.listening == True:
            data = connection.recv(1024)
            if not data:
                self.close_client(id)
                return
            else:
                data = data.decode()
                print(data)
                if "{" in data and "}" in data:
                    self.coms.incoming_dict(id, data)
                else:
                    self.coms.incoming_data(id, data)

    @threaded
    def admin_client(self, id, connection):
        while self.listening == True:
            data = connection.recv(1024)
            if not data:
                self.close_client(id)
                return
            else:
                data = data.decode()
                print(data)
                if "{" in data and "}" in data:
                    self.adcoms.incoming_dict(id, data)
                else:
                    self.adcoms.incoming_data(id, data)

class HeartBeat():
    def __init__(self, client, admin):
        self.beat_delay = 5
        self.run(client)
        self.run(admin)

    @threaded
    def run(self, server):
        while server.listening == True:
            if len(server.clients.keys()) == 0:
                time.sleep(self.beat_delay)
            else:
                if server.admin == False:
                    for each in server.clients.keys():
                        if "data" in server.clients[each]:
                            if server.clients[each]["data"] != {}:
                                server.coms.update_state(each)
                            else:
                                server.send_message(str(each), '{"commands":{"request_inital":[1]}}'+"\n")
                else:
                    for each in server.clients.keys():
                        server.adcoms.return_devices(each, "")
                time.sleep(self.beat_delay)

server = Server("0.0.0.0", 5050, "my.crt", "my.key", False, None)
server.StartServer()
adminserver = Server("0.0.0.0", 5051, "my.crt", "my.key", True, server)
adminserver.StartServer()
heart = HeartBeat(server, adminserver)
