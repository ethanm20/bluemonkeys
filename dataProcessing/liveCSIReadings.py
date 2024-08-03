import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTpyMQTT

#--------------------------------------------------------------------
# AWS MQTT CONFIGURATION
#-------------------------------------------------------------------

# Client configuration with endpoint and credentials
myClient = AWSIoTpyMQTT.AWSIoTMQTTClient("iotconsole-ffb21e69-bfb3-46d4-b53e-770684c37161")
myClient.configureEndpoint('a9p2nsgtl0l6h-ats.iot.ap-southeast-2.amazonaws.com',8883)
myClient.configureCredentials("AmazonRootCA1.pem","f088a7673ecd96e624c3e6e9b83de37442691e15ffbee24fd694ed966832dc94-private.pem.key","f088a7673ecd96e624c3e6e9b83de37442691e15ffbee24fd694ed966832dc94-certificate.pem.crt")
myClient.configureConnectDisconnectTimeout(10)

myClient.connect()

def send_mqtt_message(predicted_temp = -1, fire_alarm = -1):
    # fire_alarm Should be 1 for ON
    # fire_alarm should be either 0 or -1 for OFF
    # predicted_temp should be number of the predicted temperature in Celcius
    payload = {
        "temperature_predicted": predicted_temp,
        "fire_alarm": fire_alarm
    }

    myClient.publish("test/comp6733", json.dumps(payload), 0)

#TODO: EXAMPLE 30 Degrees, Fire Alarm On
send_mqtt_messsage(30, 1)



myClient.subscribe("test/comp6733", 0, new_mqtt_message)



