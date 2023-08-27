import subprocess
import sys

class Plugin():
    def __init__(self, config):
        self.text = ""

    def test(self, data):
        if "text" in data:
            self.text = data["text"]
            print(data["text"])

    def execute(self, data):
        if "command" in data and "parameters" in data:
            command = data["parameters"].split("@")
            command.insert(0, data["command"])
            subprocess.run(command)

    def get_states(self):
        return {
            "text": self.text
            }
    def return_functions(self):
        return {
            "test": [self.test, [ ["String","text","text for function"] ] ],
            "run_command": [self.execute, [ ["String", "command", "command to execute"], ["String", "parameters", "parameters for command, seperate with @"] ]]
        }
