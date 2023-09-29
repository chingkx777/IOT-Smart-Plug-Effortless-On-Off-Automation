from data_log import Sync
from checker import ckr
import time
import uasyncio as asyncio
from button import ButtonOnOff
from oled import oled
from hcsr04 import HCSR04

# Sensor
sensor = HCSR04(trigger_pin=5, echo_pin=18, echo_timeout_us=10000)

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
z = ButtonOnOff(button, pin)

class SensorHandler:
    def __init__(self):
        self.sensor_value = 0
        self.threshold = 5
        self.switch_to_app = asyncio.Event()
        self.switch_to_button = asyncio.Event()
    
    async def app_run(self):
        while True:
            self.sensor_value = sensor.distance_cm()
            if self.sensor_value <= self.threshold:
                print("\nSwitching to button coroutine")
                oled([['<<<Button Mode>>>', 20]])
                self.switch_to_button.set()
                await self.switch_to_app.wait()
                self.switch_to_app.clear()
            else:
                y.status(x.pin())
                command = y.text()
                x.msg(command)
    
    async def button_run(self):
        while True:
            self.sensor_value = sensor.distance_cm()
            if self.sensor_value > self.threshold:
                print("\nSwitching to app coroutine")
                oled([['<<<<App Mode>>>>', 20]])
                self.switch_to_app.set()
                await self.switch_to_button.wait()
                self.switch_to_button.clear()
            else:
                z.check_buttons()
                await asyncio.sleep_ms(100)

async def main():
    sensor_handler = SensorHandler()
    await asyncio.gather(sensor_handler.app_run(), sensor_handler.button_run())

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('I am going under maintenance......')
    y.close()
