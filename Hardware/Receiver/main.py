from data_log import Sync
from checker import ckr
import time
import uasyncio as asyncio
from oled import oled

# List all input and output name and gpio
appliances = ['light', 'fan', 'aircon', 'music']
pin = [23, 22, 21, 19]
button = [12, 13, 14, 27]

ssid_pc = '192.168.1.6'
port = 8080

oled([["", 20]])
x = ckr(appliances, pin)
x.my_dict()
y = Sync(ssid_pc, port) 
                
while True:
    try:
        y.status(x.pin())
        command = y.text()
        x.msg(command)
    except KeyboardInterrupt:
        print('I am going under maintenance......')
        y.close()
        break
