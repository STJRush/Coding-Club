import bme280
import smbus2
import smbus
import sys
import os
from datetime import datetime, timedelta
from apds9960.const import *
from apds9960 import APDS9960

from pygame import mixer 
from time import sleep
mixer.init()

import RPi.GPIO as GPIO  
GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering   
GPIO.setup(17, GPIO.OUT)   # set GPIO17 as an output (LED)  

import Adafruit_DHT as DHT
port = 1


#light stuff
bus2 = smbus.SMBus(port)
apds = APDS9960(bus2)

address = 0x77 # Adafruit BME280 address. Other BME280s may be different
bus = smbus2.SMBus(port)


apds.enableLightSensor()


def readLight():
    lighting = apds.readAmbientLight()
    print("Light: " , lighting)
    sleep(1)
    return lighting


def get_humidity():
    humid, temp = DHT.read_retry(DHT.DHT11, 4)
    print(temp, humid)
    
    return humid


def fade_in_music():
    
    print("Music fading in")
    
    mixer.music.play()
    for x in range(100):
        volume = x/100
        mixer.music.set_volume(volume)  
        sleep(0.1)
        print(volume)
        
def fade_out_music():
    #there is an inbuilt pygame fadeout but I didn't like it
    print("Music fading out")
    
    for x in range(100):
        volume = x/100
        mixer.music.set_volume(1-volume)  
        sleep(0.1)
        print(1-volume)
        
    mixer.music.stop()


#choose music
mixer.music.load("halo_choir.mp3") # This .mp3 needs to be in the same folder as your .py python file
mixer.music.set_volume(0) 

music_playing_flag = False

print("The current humidity is ", get_humidity())
print("The current light is is ", readLight())

checkHumidityOnlyEvery10Times = 0



try:  
    while True:            # This will carry on until you hit CTRL+C
        
         # Iterates up to ten before resetting
         checkHumidityOnlyEvery10Times +=1
         
         # When it gets to ten
         if checkHumidityOnlyEvery10Times % 10 == 0:
             
             # Check the humidity is nice and high
             if get_humidity() > 50:
                
                # reset the humidty counter from 10 back to 0
                checkHumidityOnlyEvery10Times = 0
                
                # Check the light sensor on GPIO 4. "0" means light detected.
                if readLight() > 1000:
                    print("SunLight Detected, playing music.")
                    
                    # Only fade in if not already playing
                    if music_playing_flag == False:
                        GPIO.output(17, 1)  # Turn on LED on GPIO 17
                        fade_in_music()
                    
                            
                    elif music_playing_flag == True:
                        print("Sunny but music already playing, no fade in needed")
                    
                    # Sets the flag to playing so it doesn't keep fading in again
                    music_playing_flag = True
                    
                # Checks for sunlight on GPIO 4. "1" means bright sunlight not detected.  
                elif GPIO.input(4) == 1:
                    
                    print("No sunlight, no music.")
                    if music_playing_flag == True:
                        GPIO.output(17, 0) # Turn off LED on GPIO 17
                        fade_out_music()
                    
                    # Sets a flag to false so it doesn't keep fading out again and again.
                    music_playing_flag = False
                            
                sleep(1) # Wait 1 seconds because a delay here MIGHT help stability.
                
                # Helps me debug the flag
                print("Music playing flag is ", music_playing_flag)

# this block will run no matter how the try block exits
finally:                     
    GPIO.cleanup()
    mixer.music.stop()
    
