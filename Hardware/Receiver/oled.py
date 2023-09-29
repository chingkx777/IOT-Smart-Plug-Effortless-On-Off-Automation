from machine import Pin, SoftI2C
from time import sleep
import ssd1306

class oled:
    def __init__(self, input_lists):
        # Initialize OLED Pin
        i2c = SoftI2C(scl=Pin(4), sda=Pin(15))

        # OLED Width and Height
        oled_width = 128
        oled_height = 64

        # Create object from class ssd1306
        oled_obj = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

        # In specific location, create word
        oled_obj.text('IOT Smart Plug', 0, 0)
        
        # Iterate through the list of input_lists and display text at specified lines
        for input_list in input_lists:
            if len(input_list) == 2:
                text, line = input_list
                oled_obj.text(text, 0, line)
        
        oled_obj.show()
