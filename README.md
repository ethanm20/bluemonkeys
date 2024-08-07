# COMP6733 Project - Blue Monkeys Team
<strong><em> Fire Monitoring Using WiFi CSI </em></strong> <br>
<strong>Authors: <em>Amy Willing, Jason Jeon, Ethan Marlow, Hayden Zhang</em></strong><br>
<strong>Monday 5th August 2024</strong><br>

## Background
In this project we aim to detect fires using WiFi Channel State Information (CSI). Recent literature suggests that for every increase of 1 degree Celcius in temperature, CSI amplitude as an average over all subcarriers reduces by 13. Using this inverse correlation we use a Linear Regression model to attempt to predict the temperature of a room using WiFi CSI and if the predicted temperature is abnormally high, a fire alarm will be activated.

## Components of Project
There are two core components of the project:
- **Training Data Collection:** The collection of training data for the model by collecting data on CSI at different room temperatures and different distances.
- **Live Temperature & Fire Prediction:** Predicting the temperature based upon the current WiFi CSI amplitude and activating the fire alarm if the temperature is abnormally high.

## Training Data Collection
- **CSI Data:** All training data is collected in the ***dataCollection*** folder as .pcap or .csv files with each row representing the individual packets received by the receiving Raspberry Pi using the Nexmon CSI library. In addition there is also some sample data in the ***sampleData*** folder.
- **Temperature Data:** Temperature readings are stored in the ***tempDetection*** folder including the Python code used to obtain temperature readings from the Arduino Nano BLE device.

## Live Temperature & Fire Prediction
The live temperature and fire prediction component consists of three modules:
1. **Live CSI Amplitude Collection:** The code for retrieving live packets from Nexmon CSI and processing the packets to retrieve the current live CSI amplitude is located at ***dataProcessing/csiLiveData4.py***. This Python script is executed on a Raspberry Pi with Nexmon CSI installed and sends the live CSI amplitude over MQTT to Module 2 below.
2. **Temperature Prediction using Linear Regression Model:** The Linear Regression model code is located in the ***dataProcessing/datap.py*** file. This script is run on a laptop due to processing power requirements and predicts the temperature based on the live CSI data from the Raspberry Pi and whether the fire alarm should be set and then notifies the fire alarm (Module 3 below) over MQTT. 
3. **Fire Alarm:** The code for the fire alarm is contained in the ***dataProcessing/fireAlarm.py*** file which is executed on a Raspberry Pi 1B. This Python script retrieves MQTT packets sent by Module 2 above that contain the predicted temperature and whether the fire alarm is activated or not. Using data from these MQTT packets, the fire alarm displays relevant data on the LCD screen and if the fire alarm is set also sets the buzzer to beep. 
