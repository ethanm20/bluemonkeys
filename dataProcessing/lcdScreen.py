import time
#import Adafruit_CharLCD as LCD

import board
import digitalio
import adafruit_character_lcd.character_lcd as character_lcd

#lcd_rs = digitalio.DigitalInOut


#PINS

#lcd_rs = 25   #GPIO 25 (Pin 22)    #RS (Board 8)          #26 #15
#lcd_en = 24   # GPIO 24 (Pin 18)   #Enable (Board 9)      #19 #11

#lcd_d4 = 23   # GPIO 23 (Pin 16)   #D4 (Board 4)          #25  #22
#lcd_d5 = 17   # GPIO 17 (Pin 11)   #D5 (Board 5)          #24   #18
#lcd_d6 = 21   # GPIO 18 (Pin 12)   #D6 (PCM_CLK) (Board 6)#22   16
#lcd_d7 = 22   # GPIO 22 (Pin 15)   #D7 (Board 7)          #27   12
#lcd_backlight = 4   #7

lcd_rs = digitalio.DigitalInOut(board.D22)
lcd_en = digitalio.DigitalInOut(board.D17)

lcd_d4 = digitalio.DigitalInOut(board.D25)
lcd_d5 = digitalio.DigitalInOut(board.D24)
lcd_d6 = digitalio.DigitalInOut(board.D23)
lcd_d7 = digitalio.DigitalInOut(board.D18)





#COL X ROWS
lcd_columns = 16
lcd_rows = 2

lcd = character_lcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

lcd.message = 'HelloHw'

#For 5 s
time.sleep(5)


lcd_rs.direction = digitalio.Direction.OUTPUT
lcd_en.direction = digitalio.Direction.OUTPUT

lcd_d4.direction = digitalio.Direction.OUTPUT
lcd_d5.direction = digitalio.Direction.OUTPUT
lcd_d6.direction = digitalio.Direction.OUTPUT
lcd_d7.direction = digitalio.Direction.OUTPUT



db = 10log10(raw)

db/10 = log10(raw)

raw = 10 ^ (db/10)