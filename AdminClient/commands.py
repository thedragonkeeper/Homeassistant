
class Commands():
    def __init__(self, client):
        self.client = client

    def client_in(self, data):
        if "Clients" in data.keys():
            self.client.devices = data["Clients"]

    def triggerfunc(self, data):
        func = data[0]
        id = data[1]
        dict = {"commands":{
            "call_function": [id, func]
            }}
        self.client.senddata(str(dict).replace("'",'"'))
    def triggerstatechange(self, id, each, new_values):
        dict = {"commands":{
            "state_change": [id, each, new_values]
            }}
        self.client.senddata(str(dict).replace("'",'"'))
