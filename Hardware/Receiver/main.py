from data_log import Sync
from checker import ckr
import time

appliances = ['light', 'fan', 'aircon']
pin = [23, 22, 21]

x = ckr(appliances, pin)
x.my_dict()
y = Sync(8080)

while True:
    try:
        command = y.text()
        x.msg(command)
    except KeyboardInterrupt:
        print('I am going under maintainence......')
        y.close()
        break
