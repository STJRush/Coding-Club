# This is for a mini greenhouse so that I can put indoor plants outside.
# An RPi controls a little heater through a relay. 
# This warms things up on frosty nights. 
# It also has a fan that turns on if it gets too hot.
# A sensor monitors and logs temperature to a csv file so that I can fine tune things.

# REQUIREMENTS: sudo pip3 install RPi.bme280



import bme280
import smbus2
import smbus
import sys
import os
import RPi.GPIO as GPIO
import csv
from datetime import datetime, timedelta

from apds9960.const import *
from apds9960 import APDS9960



from time import sleep     # this lets us have a time delay (see line 15)  
GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering  
GPIO.setup(23, GPIO.OUT)    # set GPIO25 as FAN
GPIO.setup(24, GPIO.OUT)   # set GPIO24 as RELAY

GPIO.setup(14, GPIO.OUT)    # red led
GPIO.setup(15, GPIO.OUT)   # green led
GPIO.setup(18, GPIO.OUT)    # blue led


port = 1
address = 0x77 # Adafruit BME280 address. Other BME280s may be different
bus = smbus2.SMBus(port)

#light stuff
bus2 = smbus.SMBus(port)
apds = APDS9960(bus2)
port = 1
address = 0x77 # Adafruit BME280 address. Other BME280s may be different
bus = smbus2.SMBus(port)


#light stuff
bus2 = smbus.SMBus(port)
apds = APDS9960(bus2)

apds.enableLightSensor()

def flashRedLED():
    GPIO.output(14, 1)
    sleep(0.5)
    GPIO.output(14, 0)
    sleep(0.5)
    
def flashGreenLED():
    GPIO.output(15, 1)
    sleep(0.5)
    GPIO.output(15, 0)
    sleep(0.5)
    
def flashBlueLED():
    GPIO.output(18, 1)
    sleep(0.5)
    GPIO.output(18, 0)
    sleep(0.5)
    
def flashYellowLED():
    GPIO.output(14, 1)
    GPIO.output(15, 1)
    sleep(0.5)
    GPIO.output(14, 0)
    GPIO.output(15, 0)
    sleep(0.5)
    
def flashCyanLED():
    GPIO.output(18, 1)
    GPIO.output(15, 1)
    sleep(0.5)
    GPIO.output(18, 0)
    GPIO.output(15, 0)
    sleep(0.5)
    
    
def flashMagentaLED():
    GPIO.output(18, 1)
    GPIO.output(14, 1)
    sleep(0.5)
    GPIO.output(18, 0)
    GPIO.output(14, 0)
    sleep(0.5)

def readHumidity():
    bme280_data = bme280.sample(bus,address)
    humidity  = bme280_data.humidity
    print("Humidity:" , humidity)
    sleep(1)
    return humidity

def readPressure():
    bme280_data = bme280.sample(bus,address)
    pressure  = bme280_data.pressure
    print("Pressure: ", pressure)
    sleep(1)
    return pressure

def readTemperature():
    bme280_data = bme280.sample(bus,address)
    ambient_temperature = bme280_data.temperature
    print("Temp: " , ambient_temperature)
    sleep(1)
    return ambient_temperature

def readLight():
    lighting = apds.readAmbientLight()
    print("Light: " , lighting)
    sleep(1)
    return lighting


def measure_CPUtemp(): #cpu temps inside the pi
        temp = os.popen("vcgencmd measure_temp").readline()
        return (temp.replace("temp=",""))

def create_CSV():
    path = "gardenData.csv"  #your file name, will create or overwrite.
    f = open(path, "w", newline='')

    csver = csv.writer(f)

    csver.writerow(["Date", "Temperature", "Pressure", "Humidity", "Light Level", "HeatedFlag", "FanFlag"])

    f.close()
    
    print("CSV Setup Complete")

def update_CSV():
    print("Saving to csv")
    path = "gardenData.csv"  #your file name, will create or overwrite.
    f = open(path, "a", newline='')

    csver = csv.writer(f)

    csver.writerow([datetime.now(), readTemperature(), readPressure(), readHumidity(), readLight(),heatflag, fanflag])

    f.close()
          
    print("Saving complete")
    

def blowFanFor10seconds():
    GPIO.output(23, 1)
    sleep(10)
    GPIO.output(23, 0)

    
def heaterOnFor10seconds():
    GPIO.output(24, 1)
    sleep(10)
    GPIO.output(24, 0)



#bme280.load_calibration_params(bus,address)

print("Starting up")
flashRedLED()
flashGreenLED()
flashBlueLED()
flashYellowLED()
flashCyanLED()
flashMagentaLED()

create_CSV()

try:  

    while True:
        print("Getting data")
        bme280_data = bme280.sample(bus,address)

        readTemperature()
        readPressure()
        readHumidity()
        readLight()
        print("Raspberry Pi CPU temp is..")
        print(measure_CPUtemp())
        
        #TOO COLD
        
        if readTemperature() < 5:
            
            print("Too cold! Turning on the heat!")
            flashBlueLED()
            flashBlueLED()
            flashBlueLED()
            
            flashYellowLED()
            heaterOnFor10seconds()
            
            print("Turning off the heat!")
            sleep(1)
            print("Giving it 10 seconds before checking again...")
            sleep(10)
            
            heatflag=1
            fanflag=0
        
        
        #JUST RIGHT
            
        elif readTemperature() > 5 and readTemperature() < 28:
            
            print("Temperature is nominal.")
            flashGreenLED()
            
            print("Giving it 10 seconds before checking again...")
            sleep(10)
            
            heatflag=0
            fanflag=0
        
        
        #TOO HOT !!!
       
        elif readTemperature() > 28:
            
            print("Temperature is TOO HOT! Turning on the fan")
            flashRedLED()
            flashRedLED()
            flashRedLED()
            
            blowFanFor10seconds()
            
            print("Turning off the heat!")
            sleep(1)
            print("Giving it 10 seconds before checking again...")
            sleep(10)

            heatflag=0
            fanflag=1
        
        else:
            
            print("Else? Well you shouldn't get to this line of code. Oh dear. Pack your bags.")
            
        update_CSV()

      
      
finally:                   # this block will run no matter how the try block exits  
    GPIO.cleanup()  

