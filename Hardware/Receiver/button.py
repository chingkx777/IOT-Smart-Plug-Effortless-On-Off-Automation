import machine
import time
import _thread

class button:
    def __init__(self, button_pins, led_pins):
        # Define pin and button lists
        self.led_pins = [machine.Pin(pin_num, machine.Pin.OUT) for pin_num in led_pins]
        self.button_pins = [machine.Pin(button_num, machine.Pin.IN, machine.Pin.PULL_UP) for button_num in button_pins]

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
        self.running = True
        while self.running:
            for i in range(len(self.button_pins)):
                if not self.debounce(i) and self.last_button_states[i]:
                    # Button was pressed
                    led = self.led_pins[i]
                    led.value(not led.value())  # Toggle the corresponding LED pin
                self.last_button_states[i] = self.button_states[i]
            time.sleep_ms(10)  # Small delay to avoid busy-waiting

    def start(self):
        _thread.start_new_thread(self.button_thread, ())

    def stop(self):
        self.running = False
