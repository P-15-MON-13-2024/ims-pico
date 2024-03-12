from mfrc522 import MFRC522
import utime
from wifi_connect import WifiHandler
import urequests
import json
import machine
from ssd1306 import SSD1306_I2C
from machine import Pin, I2C
from oled import OledHandler


serverUrl = '192.168.1.104:8000'

def get_access_token():
    # Get the unique identifier (bytes)
    unique_id = machine.unique_id()
    # Convert the bytes to a hexadecimal string
    unique_id_hex = ''.join('{:02x}'.format(x) for x in unique_id)

    try:    
        response = urequests.get(f"{serverUrl}/api/access-token/{str(unique_id_hex)}/")
        json_data = json.loads(response.text)
        if response.status_code == 401:
            print('hi')
            return None
        access_token = json_data['access_token']
        return access_token
    except:
        return None
        
    
    
def main():
    onboard_led = machine.Pin("LED", machine.Pin.OUT)
    onboard_led.off()
    reader = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=5,rst=22)

    WIDTH=128
    HEIGHT=64
    oled = OledHandler()
    oled.init_screen()
    wifiHandler = WifiHandler(ssid = 'keymii-way', password = 'wonderwall')
    oled.set_status_bar(text="Connecting", wifi_status="lost")
    oled.print("Connecting to")
    oled.print(wifiHandler.ssid,1)
    wifiHandler.connect()
    if wifiHandler.wlan.isconnected():
        oled.set_status_bar(text="Home", wifi_status="connected")
    oled.clean()
    access_token = get_access_token()
    if access_token == None:
        oled.print("Scanner",1)
        oled.print("Unauthorized",2)
        raise Exception("Scanner Unauthorized")
        return

    auth_header = {'Authorization': f'Bearer {access_token}'}    
    print("Bring TAG closer...")
    print("")
    
    while True:
        utime.sleep(0.001)
        reader.init()
        (stat, tag_type) = reader.request(reader.REQIDL)
        if stat == reader.OK:
            (stat, uid) = reader.SelectTagSN()
            if stat == reader.OK:
                card = int.from_bytes(bytes(uid),"little",False)
                serial_id = str(bytes(uid).hex()).upper()
                print("Card ID: " + serial_id)
                
                try:
                    onboard_led.on()
                    req = urequests.get(f"{serverUrl}/api/mirror/?serial={serial_id}", headers=auth_header)
                    print(json.loads(req.text))
                except KeyboardInterrupt:
                    machine.reset()
                except Exception as e:
                    print(e)
                onboard_led.off()


if __name__ == '__main__':
    main()