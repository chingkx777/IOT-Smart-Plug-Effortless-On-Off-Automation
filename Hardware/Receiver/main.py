from data_log import Sync
from checker import ckr
import time

# List all input and output name and gpio
appliances = ['light', 'fan', 'aircon', 'music']
pin = [23, 22, 21, 19]

ssid_pc = '192.168.1.6'
port = 8080

x = ckr(appliances, pin)
x.my_dict()
y = Sync(ssid_pc, port)


while True:
    try:
        y.status(x.pin())
        command = y.text()
        x.msg(command)
    except KeyboardInterrupt:
        print('I am under maintainance')
        y.close
        break
