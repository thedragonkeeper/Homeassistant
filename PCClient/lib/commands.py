import importlib

class Commands():
    def __init__(self, client, config):
        self.client = client
        self.config = config
        self.deviceinfo = { "name": "Unknown" }
        if "deviceinfo" in config:
            self.deviceinfo = config["deviceinfo"]
        self.functions = {
            "request_inital": [self.request_inital, [0]],
            "request_info": [self.request_info, [0]],
            "request_functions": [self.request_functions, [0]],
            "request_states": [self.request_states, [0]]
        }
        self.plugins = []

    def request_info(self, data):
        info = {"DeviceInfo": self.deviceinfo}
        if data == [0]:
            self.client.senddata(str(info).replace("'",'"'))
        else: return info

    def request_functions(self, data):
        mydict = {"Functions":{}}
        for each in self.functions:
            mydict["Functions"][each] = self.functions[each][1]
        if data == [0]:
            self.client.senddata(str(mydict).replace("'",'"'))
        else: return mydict

    def request_states(self, data):
        states = {}
        for each in self.plugins:
            states.update({each[0]: each[1].get_states()})
        if states != {}:
            states = {"States": states}
            if data == [0]:
                self.net.senddata(str(states).replace("'",'"'))
            else: return states

    def request_inital(self, data):
        dict1 = self.request_functions(data)
        dict2 = self.request_states(data)
        dict3 = self.request_info(data)
        dict1.update(dict2)
        dict1.update(dict3)
        self.client.senddata(str(dict1).replace("'",'"'))

    def client_in(self, data):
        print(data)
        if "commands" in data.keys():
            for each in data["commands"]:
                if each in self.functions:
                    self.functions[each][0](data["commands"][each][0])

    def import_plugin(self, filename):
        module = importlib.import_module(filename)
        if "Plugin" in dir(module):
            plugin = module.Plugin(self.config)
            functions = plugin.return_functions()
            self.functions.update(functions)
            self.plugins.append([filename, plugin])
