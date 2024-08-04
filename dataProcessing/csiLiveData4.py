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
numSamples = 50

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

    myClient.publish("test/comp6733", json.dumps(payload), 1)


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

import interleaved as decoder
import numpy as np
from scipy import stats
import pandas as pd

nulls = {
    20: [x+32 for x in [
            -32, -31, -30, -29,
                31,  30,  29,  0
        ]],

    40: [x+64 for x in [
        -64, -63, -62, -61, -60, -59, -1, 
            63,  62,  61,  60,  59,  1,  0
    ]],

    80: [x+128 for x in [
        -128, -127, -126, -125, -124, -123, -1,
            127,  126,  125,  124,  123,  1,  0
    ]],

    160: [x+256 for x in [
        -256, -255, -254, -253, -252, -251, -129, -128, -127, -5, -4, -3, -2, -1,
            255,  254,  253,  252,  251,  129,  128,  127,  5,  4,  3,  3,  1,  0 
    ]]
}

pilots = {
    20: [x+32 for x in [
        -21, -7,
        21,  7
    ]],

    40: [x+64 for x in [
        -53, -25, -11, 
        53,  25,  11
    ]],

    80: [x+128 for x in [
        -103, -75, -39, -11,
        103,  75,  39,  11
    ]],

    160: [x+256 for x in [
        -231, -203, -167, -139, -117, -89, -53, -25,
        231,  203,  167,  139,  117,  89,  53,  25
    ]]
}


def process_csi_data():
    samples = decoder.read_pcap(outputFile)
    samples = decoder.read_pcap(outputFile)
    csi_matrix = np.abs(samples.csi) # Access all CSI samples as a numpy matrix
    z_scores = np.abs(stats.zscore(csi_matrix, axis=0))
    threshold = 3
    # Identify rows with any Z-score greater than the threshold
    outlier_rows = np.any(z_scores > threshold, axis=1)

    # Filter the data to remove rows with outliers
    csi_matrix = csi_matrix[~outlier_rows]

    finite_mask = np.isfinite(csi_matrix).all(axis=1)
    csi_matrix = csi_matrix[finite_mask]
    removed_subcarriers = []
    removed_subcarriers.extend(nulls[80])
    for i in pilots[80]:
        removed_subcarriers.append(i)
    removed_subcarriers.sort(reverse=True)
    for i in removed_subcarriers:
        csi_matrix = np.delete(csi_matrix, i, 1)

    df_csi = pd.DataFrame(csi_matrix.mean(axis=1), columns=['csi'])
    # Now sending over MQTT
    print("Sending message over MQTT")
    send_mqtt_message(np.mean(df_csi.values))

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
