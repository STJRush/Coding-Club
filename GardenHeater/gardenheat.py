# This is for a mini greenhouse so that I can put indoor plants outside.
# An RPi controls a little heater with thorugh a relay. 
# This warms things up on frosty nights. 
# It also has a fan that turns on if it gets too hot.
# A sensor monitors and logs temperature to a csv file so that I can fine tune things.


import RPi.GPIO as GPIO
import csv
from datetime import datetime, timedelta
import bme280
import smbus2

from time import sleep     # this lets us have a time delay (see line 15)  
GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering  
GPIO.setup(25, GPIO.OUT)    # set GPIO25 as FAN
GPIO.setup(24, GPIO.OUT)   # set GPIO24 as RELAY


port = 1
address = 0x77 # Adafruit BME280 address. Other BME280s may be different
bus = smbus2.SMBus(port)

bme280.load_calibration_params(bus,address)

try:  

    while True:
        bme280_data = bme280.sample(bus,address)
        humidity  = bme280_data.humidity
        pressure  = bme280_data.pressure
        ambient_temperature = bme280_data.temperature
        print(humidity, pressure, ambient_temperature)
        
        #TOO COLD
        
        if ambient_temperature < 5:
            
            print("Too cold! Turning on the heat!")
            
            GPIO.output(24, 1)
            sleep(10)
            GPIO.output(24, 0)
            
            print("Turning off the heat!")
            sleep(1)
            print("Giving it 10 seconds before checking again...")
            sleep(10)
            
            heatflag=1
            fanflag=0
        
        
        #JUST RIGHT
            
            elif ambient_temperature > 5 and ambient_temperature <28:
            
            print("Temperature is nominal.")
            
            print("Giving it 10 seconds before checking again...")
            sleep(10)
            
            heatflag=0
            fanflag=0
        
        
        #TOO HOT
       
            elif ambient_temperature > 28:
            
            print("Temperature is TOO HOT! Turning on the fan")
            
            GPIO.output(25, 1)
            sleep(10)
            GPIO.output(25, 0)
            
            print("Turning off the heat!")
            sleep(1)
            print("Giving it 10 seconds before checking again...")
            sleep(10)

            heatflag=0
            fanflag=1
            

            path = "gardenData.csv"  #your file name, will create or overwrite.
            f = open(path, "w", newline='')

            csver = csv.writer(f)

            csver.writerow([datetime.now(), humidity, pressure, ambient_temperature, heatflag, fanflag])

            f.close()
      
      
    finally:                   # this block will run no matter how the try block exits  
        GPIO.cleanup()  

