from data_log import Sync
from checker import ckr
import time
import uasyncio as asyncio
from button import ButtonOnOff

# List all input and output name and gpio
appliances = ['light', 'fan', 'aircon', 'music']
pin = [23, 22, 21, 19]
button = [12, 13, 14, 27]

ssid_pc = '192.168.1.6'
port = 8080

x = ckr(appliances, pin)
x.my_dict()
y = Sync(ssid_pc, port)
z = ButtonOnOff(button, pin)

class SensorHandler:
    def __init__(self):
        self.sensor_value = 0
        self.threshold = 10
    
    # Initialize when sensor value self.sensor_value > self.threshold 
    async def app_run(self):
        while True:
            self.sensor_value = 11
            # Check if sensor_value indicates the need to switch to button_run
            if self.sensor_value <= self.threshold:
                print("\nSwitching to button coroutine")
                await self.button_run()
            else:
                # Receive message from app
                y.status(x.pin())
                command = y.text()
                x.msg(command)
    
    # Initialize when sensor value self.sensor_value <= self.threshold 
    async def button_run(self):
        while True:
            self.sensor_value = 11
            # Check if sensor_value indicates the need to switch to app_run
            if self.sensor_value > self.threshold:
                print("\nSwitching to app coroutine")
                await self.app_run()
            else:
                z.check_buttons()
                time.sleep_ms(100)

async def main():
    sensor_handler = SensorHandler()
    await asyncio.gather(sensor_handler.app_run(), sensor_handler.button_run())

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
