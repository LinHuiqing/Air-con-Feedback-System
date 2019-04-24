# MAIN - Entry point of code

#========================INITIALISATION START=================================
from time import sleep

import numpy as np
import I2C_LCD_driver
import Adafruit_DHT
import random

# Import modules - modules need to be in same folder
import ML_ALGO
import FIREBASE
#==========================INITIALISATION END=================================

#============================MAIN CODE======================================

# Initialise temp sensor and firebase
sensor = Adafruit_DHT.DHT11
pin = 4
fb = FIREBASE.firebase_data()

# Loop every 10mins
while True:
    # Initialise a new OTP
    FIREBASE.firebase_data.loginotp(fb)
    
    # Push Internal Temperature to Firebase
    humidity, temperature = Adafruit_DHT.read_retry(sensor,pin)
    fb.send_temperature(round(temperature,1))
    print("WOOOO IT'S {} DEGREE CELCIUS!".format(temperature))

    # Pull feedback and temperature data from Firebase
    temp_data, feedback_data = fb.get_temperature()
    outside_temp = round(temp_data['outside'], 1)
    inside_temp = round(temp_data['inside'], 1)
    aircon_temp = round(temp_data['aircon'], 1)

    number_hot = feedback_data['hot']
    number_cold = feedback_data['cold']
    number_ok = feedback_data['just_nice']

    # check if anyone left feedback. If not, don't append
    if (number_hot != 0) or (number_cold != 0) or (number_ok != 0):
        # Calculate Target value and Clean data
        target = (number_hot*(inside_temp+2) + number_cold*(inside_temp-2) + number_ok*(inside_temp)) / (number_hot + number_cold + number_ok)
        target = round(target, 1)
        output = "{} {} {}\n".format(target, outside_temp, inside_temp)

        print('target:', output)

        # Append output values to file for ML training
        f = open('ml_data.txt', 'a')
        f.write(output)
        f.close()


    # Read File, Retrieve values for ML
    file = open('ml_data.txt', 'r')

    array_2D = []

    for line in file:
        # create 1D array, append line to 1D array
        array_1D = []
        line = line.strip().split()
        for item in line:
            item = float(item)
            array_1D.append(item)

        # append each 1D array to a 2D array
        array_2D.append(array_1D)

    # convert to numpy 2D array
    data = np.array(array_2D)
    print(array_2D)

    file.close()
    

    #Retrieve OTP data and format for LCD display
    f03_otp = fb.OTP
    otp_display = 'OTP: {}'.format(f03_otp)

    # Call machine learning function
    machine_learning = ML_ALGO.Machine_Learning(data)
    regr = machine_learning.generateEQN()
    x1  = outside_temp             #current_outside
    x2 = inside_temp               #current_actual_inside
    prediction = machine_learning.getprediction(x1,x2)[0]

    print('Prediction:', prediction)
    prediction = str(round(prediction, 3))
    prediction_display = 'Temp: {}'.format(prediction)

    # Display on LCD
    mylcd = I2C_LCD_driver.lcd()
    mylcd.lcd_display_string(otp_display, 1, 1)
    mylcd.lcd_display_string(prediction_display, 2, 2)

    # Reset feedbacks
    fb.reset_feedback()

    # Sleep for 10mins
    sleep(30)
