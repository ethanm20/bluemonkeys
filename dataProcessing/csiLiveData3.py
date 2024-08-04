#!/usr/bin/env python3
# SENDS LIVE CSI DATA FROM RASPBERRY PI TO JASON'S LAPTOP
# OVER MQTT
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTpyMQTT
import base64
import os
import time

hexString = "KuABEQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=="
port = 5500
interfaceName = "wlan0"
numSamples = 100

outputFile = "outputCSILive.pcap"

packetCollectingTime = 30
packetProcessingTime = 10


#--------------------------------------------------------------------
# AWS MQTT CONFIGURATION
#-------------------------------------------------------------------

# Client configuration with endpoint and credentials
myClient = AWSIoTpyMQTT.AWSIoTMQTTClient("iotconsole-ffb21e69-bfb3-46d4-b53e-770684c37161")
myClient.configureEndpoint('a9p2nsgtl0l6h-ats.iot.ap-southeast-2.amazonaws.com',8883)
myClient.configureCredentials("AmazonRootCA1.pem","f088a7673ecd96e624c3e6e9b83de37442691e15ffbee24fd694ed966832dc94-private.pem.key","f088a7673ecd96e624c3e6e9b83de37442691e15ffbee24fd694ed966832dc94-certificate.pem.crt")
myClient.configureConnectDisconnectTimeout(10)

myClient.connect()
print("Connected to MQTT client")

def send_mqtt_message(csi_amplitude_list):
    # csi_amplitude_list is simply a list of CSI Amplitudes per packet, in order of packet number from the pcap file
    
    payload = {
        "csi_amplitude_list": csi_amplitude_list,
	"fire_alarm": -1,
	"temperature_predicted": -1
    }

    myClient.publish("test/comp6733", json.dumps(payload), 0)


#--------------------------------------------------------------------
# NEXMON CSI CONFIGURATION
#-------------------------------------------------------------------

def initial_nexmon_setup():
    print("CONFIGURING NEXMON...")
    os.system(f"ifconfig {interfaceName} up")
    time.sleep(5)

    os.system(f"nexutil -I {interfaceName} -s 500 -b -l 34 -v {hexString}")
    time.sleep(5)

    os.system(f"iw dev {interfaceName} interface add mon0 type monitor")
    time.sleep(5)

    os.system(f"ip link set mon0 up")
    time.sleep(5)

    print("NEXMON SETUP COMPLETE")


#--------------------------------------------------------------------
# CSI PROCESSING (CSI KIT) CONFIGURATION
#-------------------------------------------------------------------

def process_csi_data():
    print("Opening output file")
    with open (outputFile, 'rb') as file:
        data = file.read()
        encoded_data = base64.b64encode(data)
        
    csi_amplitude_list = str(encoded_data)

    # Now sending over MQTT
    print("Sending message over MQTT")
    send_mqtt_message(csi_amplitude_list)

#MAIN THREAD
def main():
    #Setup Nexmon Only Once
    initial_nexmon_setup()

    #Every 40 Seconds
    while True:
        
        # Save samples to outputCSILive.pcap
        os.system(f'tcpdump -i {interfaceName} dst port {str(port)} -vv -w {outputFile} -c {str(numSamples)}')

        process_csi_data()

        time.sleep(packetProcessingTime)

if __name__ == "__main__":
    main()
