import json
class Commands():
    def __init__(self, server):
        self.server = server

    def update_state(self, id):
        self.server.send_message(str(id), '{"commands":{"request_states":[0]}}'+"\n")

    def incoming_dict(self, id, data):
        data = json.loads(data)
        print("-")
        if "DeviceInfo" in data.keys():
            self.server.clients[str(id)]["data"]["DeviceInfo"] = data["DeviceInfo"]
        elif "DeviceInfo" not in self.server.clients[str(id)]["data"].keys():
            self.server.send_message(str(id), '{"commands":{"request_info":[0]}}'+"\n")
        if "Functions" in data.keys():
            self.server.clients[str(id)]["data"]["Functions"] = data["Functions"]
        elif "Functions" not in self.server.clients[str(id)]["data"].keys():
            self.server.send_message(str(id), '{"commands":{"request_functions":[0]}}'+"\n")
        if "States" in data.keys():
            self.server.clients[str(id)]["data"]["States"] = data["States"]

    def incoming_data(self, id, data):
        if self.server.clients[str(id)]["data"] == {}:
            self.server.send_message(str(id), '{"commands":{"request_inital":[1]}}'+"\n")
