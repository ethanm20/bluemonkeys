# COMP6733 Project - Blue Monkeys Team
<strong><em> Fire Monitoring Using WiFi CSI </em></strong> <br>
<strong>Authors: <em>Amy Willing, Jason Jeon, Ethan Marlow, Hayden Zhang</em></strong><br>

## Background
In this project we aim to detect fires using WiFi Channel State Information (CSI). Recent literature suggests that for every increase of 1 degree Celcius in temperature, CSI amplitude as an average over all subcarriers reduces by 13. Using this inverse correlation we use a Linear Regression model to attempt to predict the temperature of a room using WiFi CSI and if the predicted temperature is abnormally high, a fire alarm will be activated.

## Components of Project
There are two core components of the project:
- **Training Data Collection:** The collection of training data for the model by collecting data on CSI at different room temperatures and different distances.
- **Live Temperature & Fire Prediction:** Predicting the temperature based upon the current WiFi CSI amplitude and activating the fire alarm if the temperature is abnormally high.

## Training Data Collection

## Live Temperature & Fire Prediction
