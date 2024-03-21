from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf
import machine
import utime
from graphics import *

class OledHandler:
    _WIDTH  = 128                                            # oled display width
    _HEIGHT = 64                                             # oled display height
    i2c = None
    oled = None
    _status_bar_text = "Home"
    _wifi_status = "lost"
    _battery_level = 5
    _wifi_icon_map={
        "lost":wifi_lost_symbol_8x16_fb,
        "connected":wifi_connected_symbol_8x16_fb,
        "upload":wifi_upload_symbol_8x16_fb,
        "download":wifi_download_symbol_8x16_fb
        }
    _battery_level_map={
        0:battery_0_8x16_fb,
        1:battery_1_8x16_fb,
        2:battery_2_8x16_fb,
        3:battery_3_8x16_fb,
        4:battery_4_8x16_fb,
        5:battery_5_8x16_fb,        
        }
    
    def __init__(self,i2c_id=0,i2c_scl=Pin(21),i2c_sda=Pin(20),i2c_freq=200000,width=128,height=64):
        self.i2c = I2C(i2c_id, scl=i2c_scl, sda=i2c_sda, freq=i2c_freq)
        self._WIDTH = width
        self._HEIGHT = height
        self.oled = SSD1306_I2C(self._WIDTH, self._HEIGHT, self.i2c)                 # Init oled display
        self.oled.fill(0)
        
    def scan_i2c(self):
        print(self.i2c.scan())# Init I2C using pins GP8 & GP9 (default I2C0 pins)
        print("I2C Address      : "+hex(self.i2c.scan()[0]).upper()) # Display device address
        print("I2C Configuration: "+str(self.i2c))                   # Display 
    
    def init_screen(self, status_bar_text=None, wifi_status=None):
        self.oled.fill(0)
        self.set_status_bar(text=status_bar_text)
    
    def set_status_bar(self, text=None, wifi_status=None, battery_level=None):
        self.oled.fill_rect(0,0,self._WIDTH,9,0) # fill_rect(x,y,del_x,del_y,0)
        self._status_bar_text =  text or self._status_bar_text
        self._wifi_status = wifi_status or self._wifi_status
        self.oled.text(self._status_bar_text,0,0)
        self.oled.line(0,10,self._WIDTH-1,10,1)
        self.oled.blit(self._wifi_icon_map[self._wifi_status],self._WIDTH-16, 0)
        self._battery_level = battery_level or self._battery_level if battery_level!=0 else 0
        self.oled.blit(self._battery_level_map[self._battery_level],self._WIDTH-40,0)
        self.show()

    def print(self, text, x, y):
        self.oled.fill_rect(x,y+12,self._WIDTH, y+21,0)
        self.oled.text(text, x, y+12)
        self.show()
    
    def print(self, text, line=0):
        y=12+9*line
        self.oled.fill_rect(0,y,self._WIDTH, 9,0)
        self.oled.text(text, 0, y)
        self.show()
    
    def clean(self, line=None):
        if line == None: 
            self.oled.fill_rect(0, 12, self._WIDTH, self._HEIGHT-9, 0)
        else:
            y=12+9*line
            self.oled.fill_rect(0,y,self._WIDTH, 9,0)
        self.show()
    def graphic(self, fb, x, y):
        self.oled.blit(fb, x, y)
        self.show()
        
    def show(self):
        self.oled.show()
    
if __name__ == "__main__":
    oled = OledHandler()
    oled.init_screen(status_bar_text="Home")
    utime.sleep(2)
    arr = [5,4,3,2,1,0]
    for i in arr:
        oled.set_status_bar(battery_level=i)
        utime.sleep(2)