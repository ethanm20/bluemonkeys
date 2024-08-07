# COMP6733 Project - Blue Monkeys Team
<strong><em> Fire Monitoring Using WiFi CSI </em></strong> <br>
<strong>Authors: <em>Amy Willing, Jason Jeon, Ethan Marlow, Hayden Zhang</em></strong><br>

## Background
In this project we aim to detect fires using WiFi Channel State Information (CSI). Recent literature suggests that for every increase of 1 degree Celcius in temperature, CSI amplitude as an average over all subcarriers reduces by 13. Using this inverse correlation we use a Linear Regression model to attempt to predict the temperature of a room using WiFi CSI and if the predicted temperature is abnormally high, a fire alarm will be activated.

## Components of Project
There are four core components of the project:
** 

## Repository Structure
This repo is for code used in the project and also any other important relevant docs etc.

There are 3 folders :

*dataCollection: Code for the data collection stage when we are simply collecting the data that will be used in the model.

*tempDetection: Code for the temperature detection stage when we are able to deduce the temperature based upon the training data of the model using WiFI CSI.

*docs: Any useful docs or other information relevant to the project. 
