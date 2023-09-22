from machine import Pin

class ckr:
    def __init__(self, a_list, p_list):
        # Get appliances and pins list
        self.a_list = a_list
        self.p_list = p_list
        
        # Check both lists
        if len(self.a_list) == len(self.p_list):
            for item in self.a_list:
                if self.a_list.count(item) > 1:
                    raise ValueError(f'Duplicate appliances {item}')
                    break
                for item in self.p_list:
                    if self.p_list.count(item) > 1:
                        raise ValueError(f'Duplicate pin {item}')
                        break
                    
            # Dictionary <Appliance : Pin_Output>
            self.dict = dict(zip(self.a_list, self.p_list))
        else:
            raise ValueError('List provided were not the same')
        
        
    # Display Dictionary
    def my_dict(self):
        print(self.dict)


    # Check message from user input
    def msg(self, string):
        part = string.split(' ')
        part_copy = part.copy()  
        for item in part:
            if item == 'on':
                part_copy.remove('on') 
                for app in part_copy:
                    if app in self.dict:
                        self.port_On_Off(app, self.dict[app], 1)
                        print(f'{app} has turned on')
                        break
                    elif part_copy.index(app) == len(part_copy) - 1:
                        print(f'Invalid Message, {app} not registered')
                        break
                    else:
                        continue
            elif item == 'off':
                part_copy.remove('off')
                for app in part_copy:
                    if app in self.dict:
                        self.port_On_Off(app, self.dict[app], 0)
                        print(f'{app} has turned off')
                        break
                    elif part_copy.index(app) == len(part_copy) - 1:
                        print(f'Invalid Message, {app} not registered')
                        break
                    else:
                        continue
            elif part.index(item) == len(part) - 1:
                print(f'Invalid Message: {string}')
            else:
                continue
            break

    # Port ON/OFF
    def port_On_Off(self, app, pin, action):
        led_pin = Pin(pin, Pin.OUT)
        if action == 1:
            print(f"Turning on {app} in pin {pin}")
            led_pin.on()
        elif action == 0:
            print(f"Turning off {app} in pin {pin}")
            led_pin.off()
