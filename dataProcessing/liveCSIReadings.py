import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTpyMQTT

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


