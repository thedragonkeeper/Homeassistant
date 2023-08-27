import sys
sys.path.insert(0,'lib/')
import os
libraries = []
for file in os.listdir("lib/"):
    if file.endswith(".py"):
        libraries.append(file)
import json
import mynetwork
import time

class Main():
    def __init__(self, config):
        self.config = config
        if "Network" in config:
            if "SSID_PASS" in config["Network"] and "SSID" in config["Network"]:
                self.ssid = config["Network"]["SSID"]
                self.ssidpass = config["Network"]["SSID_PASS"]
            else:
                return
        else:
            return
        self.client = None
        self.trigger_net() 
        self.load_modules()
        self._Run()
    
    def trigger_net(self):
        self.net = mynetwork.Network(self.ssid, self.ssidpass)
        self.net.station_mode()
        self.net.connect()
        self.ip = self.net.get_info()
        while self.ip == "not connected":
            self.ip = net.get_info()
        if self.client == None:
            self.set_client()

    def set_client(self):
        config = self.config
        if 'config' in config:
            if "use_Client" in config['config']:
                if config['config']["use_Client"] == True:
                    if "Client.py" in libraries:
                        from Client import Client
                        if "SERVER_PEM" in config['Network'] and "SERVER_PEM" in config['Network'] and "SERVER_PORT" in config['Network']:
                            self.client = Client(config['Network']['SERVER_HOST'], config['Network']['SERVER_PORT'], config['Network']['SERVER_PEM'], config)
                            self.client.ConnectToServer()

    def load_modules(self):
        config = self.config
        if 'config' in config:  
            for each in config['config']:
                if each != "use_Client":
                    if config['config'][each] == True:
                        filename = str(each).replace("use_","")
                        if filename+".py" in libraries:
                            self.client.commands.import_plugin(filename)
    def test_net(self):
        if self.net == None:
            self.trigger_net()
        elif self.net.isconnected() == False:
            self.trigger_net()

    def check_logic(self):
        if self.client.connected == False:
            check = self.client.ConnectToServer()
            if check == 1:
                return
            elif check == 23:
                sys.exit()
            self.client.senddata("connected")
        else:
            while self.client.connected == True:
                data = self.client.RecieveData()
                if data != b"" and data != None:
                    data = data.decode('utf-8')
                    self.client.commands.client_in(data)
                
    def _Run(self):
        while True:
            time.sleep(3)
            self.test_net()
            if self.net != None:
                self.check_logic()
                print("loop")

if __name__ == "__main__":
    configfile = open('config.ini')
    config = json.loads(configfile.read())
    main = Main(config)
