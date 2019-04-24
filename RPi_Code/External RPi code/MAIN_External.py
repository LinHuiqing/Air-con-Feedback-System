#============================INITIALISATION START===============================
import Adafruit_DHT
from time import sleep

# Import Module
import FIREBASE
#============================INITIALISATION END================================

#==================================MAIN=========================================
# Initialise sensor, pin and firebase
sensor = Adafruit_DHT.DHT22
pin = 4
firebase = FIREBASE.firebase_data()

# loop to update external temperature every 10 seconds
while True:
    # Read humidity and temperature from sensor
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    print(temperature)
    temperature = round(temperature, 1)

    # Send temperature data to firebase
    firebase.send_temperature(temperature)
    print('hi\n')
    
    sleep(10)
