import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine
import urequests
import json
import utime
from graphics import wifi_connected_symbol_8x16_fb

class WifiHandler:
    ssid=""
    password=""
    led = machine.Pin('LED', machine.Pin.OUT)
    wlan = None
    
    def __init__(self, ssid, password, oled=None):
        self.ssid = ssid
        self.password = password
        
    def connect(self):
        #Connect to WLAN
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(self.ssid, self.password)
        while self.wlan.isconnected() == False:
            self.led.value(1)  # Turn LED on
            sleep(0.1)
            self.led.value(0)  # Turn LED off
            sleep(0.1)
        print(self.wlan.ifconfig())
        
if __name__ == '__main__':
    try:
        wifiHandler = WifiHandler('keymii-way','wonderwall')
        wifiHandler.connect()
        req = urequests.get("http://192.168.1.104:8000/api/hello/")
        print(json.loads(req.text))
    except KeyboardInterrupt:
        machine.reset()
