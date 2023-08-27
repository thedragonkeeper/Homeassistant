from machine import Pin
from gpio_lcd import GpioLcd

class Plugin():
    def __init__(self, config):
        if "LCD" in config:
            configdata = config["LCD"]
        self.lines = ["",""]
        self.lcd = GpioLcd(rs_pin=Pin(configdata["rs_pin"]),
              enable_pin=Pin(configdata["enable_pin"]),
              d4_pin=Pin(configdata["d4_pin"]),
              d5_pin=Pin(configdata["d5_pin"]),
              d6_pin=Pin(configdata["d6_pin"]),
              d7_pin=Pin(configdata["d7_pin"]),
              num_lines=configdata["lines"], num_columns=configdata["cols"])

    def display_lines(self, data):
        if "line1" in data and "line2" in data:
            line1,line2 = data["line1"],data["line2"]
            self.lines = [line1, line2]
            self.lcd.clear()
            self.lcd.hide_cursor()
            self.lcd.move_to(0,0)
            self.lcd.putstr(line1)
            self.lcd.move_to(0,1)
            self.lcd.putstr(line2)

    def get_states(self):
        return {"line1": self.lines[0], "line2": self.lines[1]}

    def return_functions(self):
        return {
            "display_lines": [self.display_lines, [ ["String","line1","display on 1st line"], ["String","line2","display on 2nd line"] ] ],
        }
