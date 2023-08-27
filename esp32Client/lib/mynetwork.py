import network
import socket
import ssl

class Network():
    def __init__(self, ssid, ssidpass):
        self.netname = ssid
        self.netpass = ssidpass
    
    def station_mode(self):
        self.station = network.WLAN(network.STA_IF)
        self.station.active(True)
        
    def connect(self):
        if self.isconnected() == False:
            self.station.connect(self.netname, self.netpass)
        
    def isconnected(self):
        return self.station.isconnected()
    
    def get_info(self):
        if self.isconnected() == True:
            return self.station.ifconfig()
        else:
            return "not connected"
