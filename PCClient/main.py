import sys
sys.path.insert(0,'lib/')
import glob
libraries = glob.glob("lib/*.py")
import json

class Main():
    def __init__(self, config):
        self.load_modules(config)

    def load_modules(self, config):
        if 'config' in config:
            if "use_Client" in config['config']:
                if config['config']["use_Client"] == True:
                    if "lib/Client.py" in libraries:
                        from Client import Client
                        if "Network" in config:
                            if "SERVER_PEM" in config['Network'] and "SERVER_PEM" in config['Network'] and "SERVER_PORT" in config['Network']:
                                self.client = Client(config['Network']['SERVER_HOST'], config['Network']['SERVER_PORT'], config['Network']['SERVER_PEM'], config)
                                self.client.ConnectToServer()
            for each in config['config']:
                if each != "use_Client":
                    if config['config'][each] == True:
                        filename = str(each).replace("use_","")
                        if "lib/"+filename+".py" in libraries:
                            self.client.commands.import_plugin(filename)

if __name__ == "__main__":
    configfile = open('config.ini')
    config = json.loads(configfile.read())
    main = Main(config)
