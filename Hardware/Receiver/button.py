import machine
import time
import _thread

class button:
    def __init__(self, button_pins, led_pins, special_pin):
        # Define pin and button lists
        self.led_pins = [machine.Pin(pin_num, machine.Pin.OUT) for pin_num in led_pins]
        self.button_pins = [machine.Pin(button_num, machine.Pin.IN, machine.Pin.PULL_UP) for button_num in button_pins]
        self.special_pin = special_pin

        # Initialize variables to track button state
        self.button_states = [True] * len(self.button_pins)
        self.last_button_states = [True] * len(self.button_pins)

        # Flag to control the button thread
        self.running = False

    def debounce(self, button_index):
        # Debounce function to filter out button noise
        self.button_states[button_index] = self.button_pins[button_index].value()
        if self.button_states[button_index] != self.last_button_states[button_index]:
            time.sleep_ms(20)  # Wait for button bounce to settle
            self.button_states[button_index] = self.button_pins[button_index].value()
        return self.button_states[button_index]

    def button_thread(self):
        def all_pins_on():
            for led in self.led_pins:
                led.on()
                
        def all_pins_off():
            for led in self.led_pins:
                led.off()
        
        def get_pin_status():
            status_list = []
            for led in self.led_pins:
                status_list.append(int(led.value()))  # Append 0 for off and 1 for on
            return status_list
        
        self.running = True
        while self.running:
            for i in range(len(self.button_pins)):
                if not self.debounce(i) and self.last_button_states[i]:
                    # Button was pressed
                    led = self.led_pins[i]
                    led.value(not led.value())  # Toggle the corresponding LED pin
                self.last_button_states[i] = self.button_states[i]
            pin_value = machine.Pin(self.special_pin, machine.Pin.IN).value()
            status = get_pin_status()
            if pin_value == 1 and status == [0, 0, 0]:
                all_pins_on()
                time.sleep(1)
                continue
            elif pin_value == 1:
                all_pins_off()
                time.sleep(1)
                continue
            else:
                time.sleep_ms(10)  # Small delay to avoid busy-waiting
                continue

    def start(self):
        _thread.start_new_thread(self.button_thread, ())

    def stop(self):
        self.running = False
