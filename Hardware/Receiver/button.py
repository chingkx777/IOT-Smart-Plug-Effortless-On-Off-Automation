import time
from machine import Pin

class ButtonOnOff:
    def __init__(self, button_pin, output_pin):
        self.button_pin = button_pin
        self.output_pin = output_pin
        self.button_states = [0] * len(button_pin)  # Initialize button states to 0 (not pressed)

        # Configure button pins as input with pull-up resistor
        self.buttons = [Pin(b, Pin.IN, Pin.PULL_UP) for b in button_pin]
        self.outputs = [Pin(o, Pin.OUT) for o in output_pin]

    def check_buttons(self):
        for i, button in enumerate(self.buttons):
            current_state = button.value()
            if current_state != self.button_states[i]:
                self.button_states[i] = current_state
                if current_state == 0:  # Button pressed
                    self.toggle_output(i)

    def toggle_output(self, index):
        output = self.outputs[index]
        output.value(not output.value())
