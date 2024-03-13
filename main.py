from mfrc522 import MFRC522
import utime
from wifi_connect import WifiHandler
import urequests
import json
import machine
from ssd1306 import SSD1306_I2C
from machine import Pin, I2C
from oled import OledHandler


serverUrl = 'http://192.168.1.104:8000'
access_token = ""
auth_header = {}
onboard_led = machine.Pin("LED", machine.Pin.OUT)
oled = OledHandler()
reader = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=5,rst=22)

def get_access_token():
    unique_id = machine.unique_id()
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
        
def start_sapien_scan(reader, oled):
    while True:
        utime.sleep(0.001)
        reader.init()
        (stat, tag_type) = reader.request(reader.REQIDL)
        if stat == reader.OK:
            (stat, uid) = reader.SelectTagSN()
            if stat == reader.OK:
                card = int.from_bytes(bytes(uid),"little",False)
                serial_id = str(bytes(uid).hex()).upper()                
                try:
                    onboard_led.on()
                    res = urequests.get(f"{serverUrl}/api/get-sapien/?serial={serial_id}", headers=auth_header)
                    data = parse_sapien(res,oled)
                except KeyboardInterrupt:
                    machine.reset()
                except Exception as e:
                    print(e)
            onboard_led.off()
            
def get_sapien(serial_id):
    onboard_led.on()
    oled.set_status_bar(wifi_status="upload")
    res = urequests.get(f"{serverUrl}/api/get-sapien/?serial={serial_id}", headers=auth_header)
    oled.set_status_bar(wifi_status="connected")
    data = parse_sapien(res)
    onboard_led.off()
    return data
    
def parse_sapien(response):
    oled.clean()
    if response.status_code == 404:
        oled.print("User",0)
        oled.print("Unrecognised",1)
        return {"exists":False}
    data = json.loads(response.text)
    name = data["name"]
    insti_id = data["insti_id"]
    allowed = data["allowed"]
    oled.print("Name: "+name,0)
    oled.print("ID: "+insti_id,1)
    if not allowed:
        oled.print("[!] Not Allowed", 4)
    data["exists"]=True
    return data

def get_serial_id():
    (stat, tag_type) = reader.request(reader.REQIDL)
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        if stat == reader.OK:
            card = int.from_bytes(bytes(uid),"little",False)
            serial_id = str(bytes(uid).hex()).upper()
            return serial_id
    return None

def get_inventory_item(serial_id):
    onboard_led.on()
    oled.set_status_bar(wifi_status="upload")
    res = urequests.get(f"{serverUrl}/api/get-item/?serial={serial_id}", headers=auth_header)
    oled.set_status_bar(wifi_status="connected")
    data = parse_inventory_item(res)
    return data

def parse_inventory_item(response):
    if response.status_code == 404:
        oled.print("Item",0)
        oled.print("Unrecognised",1)
        return {"exists":False}
    data = json.loads(response.text)
    name = data["name"]
    category = data["category"]
    is_available = data["is_available"]
    oled.print("Item: "+name, 2)
    if not is_available:
        oled.print("[!] Not Allowed", 4)
    data["exists"]=True
    return data

def main():
    onboard_led.off()

    WIDTH=128
    HEIGHT=64

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
    reader.init()
    while True:
        oled.set_status_bar(text="Home")
        utime.sleep(0.001)
        sapien_serial_id = get_serial_id()
        if sapien_serial_id != None:
            sapien={"exists":False}
            try:
                sapien = get_sapien(sapien_serial_id)
            except KeyboardInterrupt:
                machine.reset()
            except Exception as e:
                oled.clean()
                oled.print("Error occurred!",0)
                oled.print("Scan again.",1)
                print(e)
            if sapien["exists"] and sapien["allowed"] :
                oled.set_status_bar(text="Issue")
                oled.print("Scan item...",4)
                item_serial_id = None
                while (item_serial_id==sapien_serial_id or item_serial_id==None):
                    utime.sleep(0.001)
                    item_serial_id = get_serial_id()
                inventory_item = {"exists":False}
                try:
                    inventory_item = get_inventory_item(item_serial_id)
                except KeyboardInterrupt:
                    machine.reset()
                except Exception as e:
                    oled.clean()
                    oled.print("Error occurred!",0)
                    oled.print("Scan again.",1)
                    print(e)
                if inventory_item["exists"] and inventory_item["is_available"]:
                    oled.print("Press (A) for ok",4)
                


if __name__ == '__main__':
    main()