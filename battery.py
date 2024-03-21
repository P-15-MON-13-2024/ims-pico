from machine import ADC
import utime

batteryIn = ADC(26)

def readBattery():
    sensorValue = batteryIn.read_u16()
    voltage = sensorValue * (3.3 / 65535)
    print(voltage)
    return voltage
    

