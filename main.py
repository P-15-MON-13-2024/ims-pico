from mfrc522 import MFRC522
import utime
from wifi_connect import WifiHandler
import urequests
import json
import machine
from ssd1306 import SSD1306_I2C
from machine import Pin, I2C
from oled import OledHandler
from graphics import option_picker_8x8_fb

wifi_configs={
    "keymii-way":["wonderwall",'http://192.168.1.104:8000'],
    "B810":["47305175",'http://192.168.0.105:8000']
    }
wifiSSID = "keymii-way"
serverUrl = wifi_configs[wifiSSID][1]

wifiPSWD = wifi_configs[wifiSSID][0] 
access_token = ""
auth_header = {}
onboard_led = machine.Pin("LED", machine.Pin.OUT)
oled = OledHandler()
reader = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=5,rst=2)
buttonA = Pin(18, Pin.IN, Pin.PULL_DOWN)
buttonB = Pin(16, Pin.IN, Pin.PULL_DOWN)

def get_access_token():
    unique_id = machine.unique_id()
    unique_id_hex = ''.join('{:02x}'.format(x) for x in unique_id)
    try:    
        response = urequests.get(f"{serverUrl}/api/rfid/access-token/{str(unique_id_hex)}/")
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
                    res = urequests.get(f"{serverUrl}/api/rfid/get-sapien/?serial={serial_id}", headers=auth_header)
                    data = parse_sapien(res,oled)
                except KeyboardInterrupt:
                    machine.reset()
                except Exception as e:
                    print(e)
            onboard_led.off()
            
def get_sapien(serial_id):
    onboard_led.on()
    oled.set_status_bar(wifi_status="download")
    res = urequests.get(f"{serverUrl}/api/rfid/get-sapien/?serial={serial_id}", headers=auth_header)
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

def get_inventory_item(serial_id, run_mode=None):
    onboard_led.on()
    oled.set_status_bar(wifi_status="download")
    res = urequests.get(f"{serverUrl}/api/rfid/get-item/?serial={serial_id}", headers=auth_header)
    oled.set_status_bar(wifi_status="connected")
    data = parse_inventory_item(res, run_mode)
    return data

def parse_inventory_item(response, run_mode):
    if response.status_code == 404:
        oled.print("Item",0)
        oled.print("Unrecognised",1)
        return {"exists":False}
    data = json.loads(response.text)
    name = data["name"]
    category = data["category"]
    is_available = data["is_available"]
    oled.print("Item: "+name, 2)
    if run_mode=="Issue" and not is_available:
        oled.print("[!] Not Available", 4)
        utime.sleep(2)
    if run_mode=="Return" and is_available:
        oled.print("[!] Not Issued", 4)
        utime.sleep(2)
    data["exists"]=True
    return data

def home_menu():
    oled.clean()
    oled.set_status_bar(text="Home")
    oled.print("Issue",1)
    oled.print("Return",3)
    s = -1
    while True:
        line = 30+9*s
        oled.graphic(option_picker_8x8_fb, 70, line)
        if buttonB.value() == 1:
            s = s*-1
            oled.oled.fill_rect(70, line, 8, 8,0)
            oled.show()
        utime.sleep(0.1)
        if buttonA.value()==1:
            break
    oled.clean()
    return "Issue" if (s==-1) else "Return"

def run_issue_mode(sapien_serial_id):
    oled.print("Scan item...",4)
    item_serial_id = None
    while (item_serial_id==sapien_serial_id or item_serial_id==None):
        utime.sleep(0.001)
        item_serial_id = get_serial_id()
    inventory_item = {"exists":False}
    try:
        inventory_item = get_inventory_item(item_serial_id, "Issue")
    except KeyboardInterrupt:
        machine.reset()
    except Exception as e:
        oled.clean()
        oled.print("Error occurred!",0)
        oled.print("Scan again.",1)
        print(e)
    if inventory_item["exists"] and inventory_item["is_available"]:
        oled.print("Press (A) for ok",4)
        while True:
            if buttonA.value() == 1:
                issue_success = handle_issue_process(sapien_serial_id, item_serial_id)
                if issue_success:
                    oled.print("[*] Issued",4)
                else:
                    oled.clean()
                    oled.print("[!] Failed",2)
                utime.sleep(2)                    
                break
            elif buttonB.value() == 1:
                oled.clean()
                oled.print("[!] Aborted")
                utime.sleep(2)
                break

def run_return_mode(sapien_serial_id):
    oled.print("Scan item...",4)
    item_serial_id = None
    while (item_serial_id==sapien_serial_id or item_serial_id==None):
        utime.sleep(0.001)
        item_serial_id = get_serial_id()
    inventory_item = {"exists":False}
    try:
        inventory_item = get_inventory_item(item_serial_id, "Return")
    except KeyboardInterrupt:
        machine.reset()
    except Exception as e:
        oled.clean()
        oled.print("Error occurred!",0)
        oled.print("Scan again.",1)
        print(e)
    if inventory_item["exists"] and not inventory_item["is_available"]:
        oled.print("Press (A) for ok",4)
        while True:
            if buttonA.value() == 1:
                return_success = handle_return_process(sapien_serial_id, item_serial_id)
                if return_success:
                    oled.print("[*] Returned",4)
                else:
                    oled.clean()
                    oled.print("[!] Failed",2)                
                utime.sleep(2)
                break
            elif buttonB.value() == 1:
                oled.clean()
                oled.print("[!] Aborted")
                utime.sleep(2)
                break

def handle_issue_process(sapien_serial_id, item_serial_id):
    oled.set_status_bar(wifi_status="upload")
    res = urequests.post(f"{serverUrl}/api/rfid/add-issue-record/",json={"sapien_id":sapien_serial_id, "item_id":item_serial_id} , headers=auth_header)
    oled.set_status_bar(wifi_status="connected")
    if res.status_code == 201:
        return True
    else:
        return False

def handle_return_process(sapien_serial_id, item_serial_id):
    oled.set_status_bar(wifi_status="upload")
    res = urequests.post(f"{serverUrl}/api/rfid/return-item/",json={"sapien_id":sapien_serial_id, "item_id":item_serial_id} , headers=auth_header)
    oled.set_status_bar(wifi_status="connected")
    if res.status_code == 200:
        return True
    else:
        return False

def main():
    onboard_led.off()

    WIDTH=128
    HEIGHT=64

    oled.init_screen()
    wifiHandler = WifiHandler(ssid = wifiSSID, password = wifiPSWD)
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
        utime.sleep(0.001)
        menu_select = home_menu()
        while True:
            oled.set_status_bar(text=menu_select)
            utime.sleep(0.001)
            oled.print("Scan ID...")
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
                    break
                if not sapien["exists"]:
                    utime.sleep(2)
                    break
                elif sapien["allowed"] :
                    if menu_select == "Issue":
                        run_issue_mode(sapien_serial_id)
                        break
                    if menu_select == "Return":
                        run_return_mode(sapien_serial_id)
                        break

while True:
    main()
    
            
