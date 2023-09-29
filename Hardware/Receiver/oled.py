from machine import Pin, SoftI2C
from time import sleep
import ssd1306

class oled:
    def __init__(self, text, line):
        self.text = text
        self.line = line
        
        # Initialize OLED Pin
        i2c = SoftI2C(scl=Pin(5), sda=Pin(18))

        # OLED Width and Height
        oled_width = 128
        oled_height = 64

        # Create object from class ssd1306
        oled_obj = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
        
        # In specific location, create word
        oled_obj.text('IOT Smart Plug', 0, 0)
        oled_obj.text(f'IP: 192.168.1.19', 0, 20)
        oled_obj.text(self.text, 0, self.line)
        
                
        oled_obj.show()
