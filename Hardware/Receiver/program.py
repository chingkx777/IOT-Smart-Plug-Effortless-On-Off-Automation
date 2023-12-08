from data_log import Sync
from checker import ckr
from oled import oled
from button import button
import time, machine, utime, json
from hcsr04 import HCSR04

# Text File saving IP Address
file_name = "ip_address.txt"

# List all input and output name and GPIO
appliances = ['light', 'fan', 'charger']
pin_list = [23, 22, 21]
button_list = [12, 13, 14]
special_pin = 26

# IP Address and port of APP(PC)
ssid_pc = '192.168.43.140'
port = 8000

x = ckr(appliances, pin_list)
x.my_dict()
y = Sync(ssid_pc, port)

with open(file_name, "r") as file:
    # Read the IP address from the file
    saved_ip_address = file.read()
    print("Saved IP address:", saved_ip_address)
    oled([[f'{saved_ip_address}', 20]])

# Define a flag to control the task_2 loop
task_2_running = False

# Define a timer to periodically check for messages
message_check_timer = time.ticks_ms()

# Function to turn all pins in the pin_list ON
def all_pins_on(my_pin_list):
    for pin_number in my_pin_list:
        pin = machine.Pin(pin_number, machine.Pin.OUT)
        pin.on()

# Function to turn all pins in the pin_list OFF
def all_pins_off(my_pin_list):
    for pin_number in my_pin_list:
        pin = machine.Pin(pin_number, machine.Pin.OUT)
        pin.off()

def task_1():
    command = y.text()
    x.msg(command)
    # Add task-specific code for task_1 here

def task_2():
    my_button = button(button_list, pin_list, special_pin)
    my_button.start()
      
    text = y.text()
    if text == 'stop':
        my_button.stop()
        y.status(x.pin())

while True:
    try:
        text = y.text()
        y.status(x.pin())

        if text == "task_1":
            oled([['[APP MODE]', 20]])
            task_1()
        elif text == "task_2":
            oled([['[BUTTON MODE]', 20]])
            task_2()
        else:
            pass
    except KeyboardInterrupt:
        print('I am under maintainance......')
        y.close()
