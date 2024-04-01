from machine import ADC
import utime

class BatteryMonitor:
    
    _batteryIn = None
    last_battery_read_time= 0;
    
    def __init__(self, Pin):
        self._batteryIn = ADC(Pin)
    
    def readBattery(self):
        sensorValue = self._batteryIn.read_u16()
        voltage = sensorValue * (3.3 / 65535)
        return voltage

    def updateBatteryLevel(self, oled):
        if utime.time()-self.last_battery_read_time>10:
            volt = self.readBattery()
            level = 5
            if volt >= 3.3:
                level = 5
            elif volt >=2.9:
                level = 4
            elif volt >=2.5:
                level = 3
            elif volt >=2.1:
                level = 2
            elif volt >= 1.8:
                level = 1
            else:
                level = 0
            oled.set_status_bar(battery_level = level)
            self.last_battery_read_time=utime.time()

