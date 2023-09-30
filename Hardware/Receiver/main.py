from data_log import Sync
from checker import ckr
from oled import oled
from button import button
import time, machine, utime, json

# Current time initialize
current_time = utime.localtime()
year, month, day, hour, minute, second, weekday, yearday = current_time

# IP Address of ESP32, time to enable button mode
file_name = "ip_address.txt"
file_name1 = "pin_status.txt"
i = 10

# List all input and output name and gpio
appliances = ['light', 'fan', 'aircon', 'music']
pin_list = [23, 22, 21, 19]
button_list = [12, 13, 14, 27]

# IP Address and port of APP(PC)
ssid_pc = '192.168.1.6'
port = 8080

oled_display = oled([["", 20]])  # Initialize OLED display
with open(file_name1, "r") as file:
    # Read the pin status from the file as a JSON string
    status_json = file.read()
        
    # Deserialize the JSON string into a list of integers
    status = json.loads(status_json)

    pin_memory = [machine.Pin(pin, machine.Pin.OUT) for pin in pin_list]

    def update_pins():
        for pin, state in zip(pin_memory, status):
            pin.value(state)

    update_pins()
    print(f'Pin Updated on {hour}:{minute}:{second} {day}/{month}/{year}')
# Initialize OLED display
oled_display = oled([
    ["Pin Updated", 20],
    [f'{hour}:{minute}:{second}', 40],
    [f'{day}/{month}/{year}', 50]
                     ]) 
x = ckr(appliances, pin_list)
x.my_dict()
y = Sync(ssid_pc, port)
controller = button(button_list, pin_list)

# Create a separate machine.Pin object for button 12 and 26
button_12_pin = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
button_26_pin = machine.Pin(26, machine.Pin.IN, machine.Pin.PULL_UP)

def task_1():
    controller.run()

def task_2():
    y.status(x.pin())
    with open(file_name1, "w") as file:
        # Serialize the list to a JSON string
        list_pin_json = json.dumps(x.pin())
        print(f'Memory Save: {list_pin_json}')
        
        # Write the JSON string to the file, overwriting existing data
        file.write(list_pin_json)
    command = y.text()
    x.msg(command)

try:
    while i != 0:
        # Read the state of button 12
        button_12_state = button_12_pin.value()
        button_26_state = button_26_pin.value()

        # Check button 26 state
        if button_26_state == 0:
            oled([["Waiting......", 20]])
            print('task 1')
            button_26_state = 1
            time.sleep(3)
            oled([["<<Button Mode>>", 20]])
            while True:
                task_1()
                button_26_state = button_26_pin.value()  # Update button_26_state
                if button_26_state == 0:
                    break
            break
                    
        else:
            oled([
                 [f'{i} second before', 20],
                 ['button mode off', 30],
                ])
            time.sleep(1)
            i -= 1
            continue

    with open(file_name, "r") as file:
            # Read the IP address from the file
            saved_ip_address = file.read()
            print("Saved IP address:", saved_ip_address)
            oled([[f'{saved_ip_address}', 20]])

    while True:
        print('task 2')
        task_2()
except KeyboardInterrupt:
    print('I am under maintenance')
    y.close()
