# Link: http://www.circuitbasics.com/raspberry-pi-i2c-lcd-set-up-and-programming/

import I2C_LCD_driver   # import module from same folder - DO NOT TOUCH MODULE
from time import *

mylcd = I2C_LCD_driver.lcd()

mylcd.lcd_display_string("Hello World!", 2, 3)
