import time

import board
import digitalio
import adafruit_character_lcd.character_lcd as character_lcd

import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTpyMQTT


#---------------------------------------------------------------------
# LCD CONFIGURATION
#---------------------------------------------------------------------

#PINS: (FOR RASPBERRY PI 1 B+)

#Pin R5 (Shield: 8) (Pi: 15)
lcd_rs = digitalio.DigitalInOut(board.D22)

#Pin EN (Shield: 9) (Pi: 11)
lcd_en = digitalio.DigitalInOut(board.D17)

#Pin D4 (Shield: 4) (Pi: 22)
lcd_d4 = digitalio.DigitalInOut(board.D25)

#Pin D5 (Shield: 5) (Pi: 18)
lcd_d5 = digitalio.DigitalInOut(board.D24)

#Pin D6 (Shield: 6) (Pi: 16)
lcd_d6 = digitalio.DigitalInOut(board.D23)

#Pin D7 (Shield: 7) (Pi: 12)
lcd_d7 = digitalio.DigitalInOut(board.D18)

#LCD Backlight (Shield: 10) (Pi: 7)
lcd_backlight = digitalio.DigitalInOut(board.D4)

#Beeper Pin (Pi: 31)
beeper_pin = digitalio.DigitalInOut(board.D7)


#Specifying all Pins as Outputs
lcd_rs.direction = digitalio.Direction.OUTPUT
lcd_en.direction = digitalio.Direction.OUTPUT

lcd_d4.direction = digitalio.Direction.OUTPUT
lcd_d5.direction = digitalio.Direction.OUTPUT
lcd_d6.direction = digitalio.Direction.OUTPUT
lcd_d7.direction = digitalio.Direction.OUTPUT

lcd_backlight.direction = digitalio.Direction.OUTPUT
beeper_pin.direction = digitalio.Direction.OUTPUT


#16 x 2 Display
lcd_columns = 16
lcd_rows = 2

#Initialising LCD
lcd = character_lcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
lcd.clear()

#------------------------------------------------------------------
# FIRE ALARM CONFIGURATION
#-------------------------------------------------------------------

#FIRE ALARM ACTIVATED
def fire_alarm(temperature):
    lcd.clear()
    msg = 'FIRE ALARM!'
    if (temperature != -1):
        msg = msg + '\nTemp: ' + str(round(temperature,2)) + 'C'
    lcd.message = msg

    #LCD Blink Here
    i = 0
    while (i < 3):
        beeper_pin.value = False
        lcd.backlight = False
        lcd.display = False

        time.sleep(0.5)

        beeper_pin.value = True
        lcd.backlight = True
        lcd.display = True

        time.sleep(0.5)

        i = i + 1
    
    lcd.backlight = True
    lcd.display = True
    beeper_pin.value = False


#-------------------------------------------------------------------
# PREDICTED TEMPERATURE CONFIGURATION
#-------------------------------------------------------------------

def display_predicted_temperature(temperature):
    lcd.clear()
    lcd.message = 'Temp: ' + str(round(temperature,2)) + 'C'


#--------------------------------------------------------------------
# AWS MQTT CONFIGURATION
#-------------------------------------------------------------------

def new_mqtt_message(client, userdata, message):
    msgPayload = message.payload
    msgPayloadStr = msgPayload.decode('utf-8')

    print('MQTT RECEIVED: MESSAGE PAYLOAD')
    print(msgPayloadStr)

    messageObj = json.loads(msgPayloadStr)

    if (messageObj['fire_alarm'] == 1):
        fire_alarm(messageObj['temperature_predicted'])
    elif (messageObj['temperature_predicted'] != -1):
        display_predicted_temperature(messageObj['temperature_predicted'])

# Client configuration with endpoint and credentials
myClient = AWSIoTpyMQTT.AWSIoTMQTTClient("iotconsole-ffb21e69-bfb3-46d4-b53e-770684c37161")
myClient.configureEndpoint('a9p2nsgtl0l6h-ats.iot.ap-southeast-2.amazonaws.com',8883)
myClient.configureCredentials("AmazonRootCA1.pem","f088a7673ecd96e624c3e6e9b83de37442691e15ffbee24fd694ed966832dc94-private.pem.key","f088a7673ecd96e624c3e6e9b83de37442691e15ffbee24fd694ed966832dc94-certificate.pem.crt")
myClient.configureConnectDisconnectTimeout(10)

myClient.connect()

myClient.subscribe("test/comp6733", 0, new_mqtt_message)

while True:
    time.sleep(5)


