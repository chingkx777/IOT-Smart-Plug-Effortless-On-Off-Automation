from machine import Pin
import time

class button_On_Off:
    def __init__(self, button_pin, output_pin):
        self.button_pin = button_pin
        self.output_pin = output_pin    

        button = Pin(self.button_pin, Pin.IN, Pin.PULL_UP)
        output = Pin(self.output_pin, Pin.OUT)

        while True:
            # Variable to track the button state and output state 
            button_state = button.value()
            output_state = output.value()
            
            # Process
            if button_state == 0: # Button Pressed
                if output_state == 0:
                    output.on()
                    time.sleep_ms(200)
                else:
                    output.off()
                    time.sleep_ms(200)
                    
# Creating Object from Class
# button_On_Off(input_pin, output_pin)
button_On_Off(25, 2)
