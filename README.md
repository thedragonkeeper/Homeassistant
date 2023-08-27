# Home assistant
This is a Python3 implemenation for controlling devices on the network.

This is highly WIP.  Very likely to break and give you a hard time.

For this to work you will need:
- Server
- AdminClient
- Client

At the moment the admin client is needed to issue commands and check states.
There are no schedules/timers. I havnt bothered making services. Threads hang out for too long. The gui sucks, idc.

The PCClient can be run on many devices (only tested on linux) and the esp32Client can be used on a esp32 device running micropython (tested on 1.20.0)

The Server runs on 2 ports, one for the clients and one for the admins. You can use the same/different networks and  same/different ssl keys. its better to use different keys.
You will need to create 1 or 2 key/crt pairs for the server and give the crt's to the adminclient and pcclient. However if you are using the esp32client the crt will need to be pem.

For the devices  (PCClient and esp32client) you will need to create a config.ini file for configuration. Here is an example for the esp32client:
```
{
"LCD": {
    "rs_pin": 19,
    "enable_pin": 23,
    "d5_pin": 17,
    "d6_pin": 16,
    "d7_pin": 15,
    "d4_pin": 18,
    "lines": 2,
    "cols": 16
    },
"SERVOS": {
    "1": {
        "name": "servo1",
        "desc": "test servo",
        "pin": 21,
        "freq": 50,
        "minangle": 0,
        "maxangle": 180
        }
    },
"config": {
    "use_Client": true,
    "use_mainlcd": true,
    "use_servos": true
    },
"deviceinfo": {
    "name": "EspTestDevice",
    "code_version": "0.1",
    "board": "esp32-wroom-32"
    },
"Network": {
    "SSID": "ssid name",
    "SSID_PASS": "ssid password",
    "SERVER_PEM": "cert.pem",
    "SERVER_HOST": "127.0.0.1",
    "SERVER_PORT": 5050
    },
}
```
The essential ones are "config" "deviceinfo" and "Network".  These define how the device functions.  
"Network" is for your WIFI and server details
"deviceinfo" can be anything you want to display your device as
"config" lists the plugins you want to use in the format  "use_"+plugin_name
The other entries are for the Plugins,  you can see mainlcd.py and servos.py  to see how they intergrate.

To create a plugin 1st start by adding it to the config under "config":
If you want a plugin called "Bash"  put "use_Bash": true 
now make a file under lib/ called Bash.py
Notice that the names match up
Now we can create a basic plugin:
```
class Plugin():
    def __init__(self, config):
        self.text = ""

    def test(self, data):
        if "text" in data:
            self.text = data["text"]  ## this is assigning the current state
            print(data["text"])

    def get_states(self):  ##this function is essential
        # a diction is returned with a list of variables and values
        #these match what you listed in the returned_functions
        return {
            "text": self.text
            }

    def return_functions(self):  ##this function is essential
      ## we return functions we can run, this lets the server know what its allowed to call
      ## the format is { "called name" : [ function [  ["TYPE", "variableName", "Variable description" ], ["TYPE", "variableName", "Variable description" ]  ] ] }  you can list as many variables as you want for each function
        return {
            "test": [self.test, [ ["String","text","text for function"] ] ]
        }

```

im bored of typing now ,  good luck with this shit show
