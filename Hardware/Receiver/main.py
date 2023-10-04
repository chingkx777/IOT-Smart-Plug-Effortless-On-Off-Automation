from data_log import Sync
from checker import ckr
from oled import oled
from button import button
import time, machine, utime, json
from hcsr04 import HCSR04

# Text File saving IP Address
file_name = "ip_address.txt"

# List all input and output name and GPIO
appliances = ['light', 'fan', 'aircon', 'music']
pin_list = [23, 22, 21, 19]
button_list = [12, 13, 14, 27]

# IP Address and port of APP(PC)
ssid_pc = '192.168.1.6'
port = 8080

x = ckr(appliances, pin_list)
x.my_dict()
y = Sync(ssid_pc, port)
controller = button(button_list, pin_list)

with open(file_name, "r") as file:
    # Read the IP address from the file
    saved_ip_address = file.read()
    print("Saved IP address:", saved_ip_address)
    oled([[f'{saved_ip_address}', 20]])

# Define a flag to control the task_2 loop
task_2_running = False

# Define a timer to periodically check for messages
message_check_timer = time.ticks_ms()

def task_1():
    command = y.text()
    x.msg(command)
    # Add task-specific code for task_1 here

def task_2():
    my_button = button(button_list, pin_list)
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
