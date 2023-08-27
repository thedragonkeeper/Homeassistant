import json
class adminCommands():
    def __init__(self, server):
        self.server = server
        self.commands = {
            "get_devices": self.return_devices,
            "call_function": self.call_func_on_id,
            "state_change": self.call_statechange_on_id
        }


    def return_devices(self, id, data):
        clients = {"Clients": {} }
        for device in self.server.client_server.clients.keys():
            clients["Clients"][device] = {
                "id": self.server.client_server.clients[device]["id"],
                "ip": self.server.client_server.clients[device]["addr"][0],
                "data": self.server.client_server.clients[device]["data"]
            }
        self.server.send_message(str(id), str(clients).replace("'",'"') )


    def call_func_on_id(self, id, data):
        print("function called")
        print(data)
        dict = {"commands":{str(data[1]):[0]}}
        self.server.client_server.send_message(str(data[0]), str(dict).replace("'",'"')+"\n")

    def call_statechange_on_id(self, id, data):
        print("state change called")
        print(data)
        client = data[0]
        data.pop(0)
        function_to_use = data[0]
        data.pop(0)
        dict = {"commands":{str(function_to_use):data}}
        self.server.client_server.send_message(str(client), str(dict).replace("'",'"')+"\n")

    def incoming_dict(self, id, data):
        data = json.loads(data)
        if "commands" in data.keys():
            for each in data["commands"]:
                self.commands[each](id, data["commands"][each])


    def incoming_data(self, id, data):
        print("incoming: "+str(data))
