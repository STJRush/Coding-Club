import bme280
import smbus2
import smbus
import sys
import os
from datetime import datetime, timedelta
from apds9960.const import *
from apds9960 import APDS9960

import board
import neopixel

from pygame import mixer 
from time import sleep
mixer.init()

import RPi.GPIO as GPIO  
GPIO.setmode(GPIO.BCM)     # set up BCM GPIO numbering   
GPIO.setup(17, GPIO.OUT)   # set GPIO17 as an output (LED)  

import Adafruit_DHT as DHT
port = 1



#https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage
pixels = neopixel.NeoPixel(board.D18, 18)


#light stuff
bus2 = smbus.SMBus(port)
apds = APDS9960(bus2)

address = 0x77 # Adafruit BME280 address. Other BME280s may be different
bus = smbus2.SMBus(port)


apds.enableLightSensor()


def readLight():
    lighting = apds.readAmbientLight()
    #print("Light: " , lighting)
    sleep(1)
    return lighting


def get_humidity():
    humid, temp = DHT.read_retry(DHT.DHT11, 4)
    #print(temp, humid)
    
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


# thanks to Adam Luchjenbroers for this mapping https://stackoverflow.com/a/1969274
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return int(rightMin + (valueScaled * rightSpan))

#choose music
mixer.music.load("halo_choir.mp3") # This .mp3 needs to be in the same folder as your .py python file
mixer.music.set_volume(0) 

music_playing_flag = False

#TEST
print("The current humidity is ", get_humidity())
print("The current light is is ", readLight())

checkHumidityOnlyEvery10Times = 0


try:  
    while True:            # This will carry on until you hit CTRL+C

        #Humidity Display
        humidityCurrent = get_humidity()
        humidityMax = 20
        humidityMin = 0

        print("The current humidity is ", humidityCurrent, "out of ", humidityMax)
        ledPosition = translate(humidityCurrent,humidityMin,humidityMax,1,18)
        print("Humidity is at ", ledPosition, " out of 18 on the wheel")
        print("")
        
        #clear all neopixels
        pixels.fill((0, 0, 0))
        
        # Blue smiley face if humidity threshold reached
        if humidityCurrent > humidityMax:
            pixels.fill((0, 0, 10))
            sleep(0.1)
            pixels[0] = (40, 40, 20)
            pixels[1] = (40, 40, 20)
            pixels[2] = (40, 40, 20)
            pixels[17] = (40, 40, 20)
            pixels[16] = (40, 40, 20)
            pixels[15] = (40, 40, 20)
            pixels[6] = (40, 40, 20)
            pixels[12] = (40, 40, 20)
        
        # Show progress to humidity threshold using LEDS
        elif humidityCurrent < humidityMax:  

            #Blue Humidity LED effect wheel
            
            # Whitey colour
            for x in range(ledPosition):
                pixels[x] = (20, 20, 40)
                sleep(0.05)
                
            # Bluey colour    
            for x in range(ledPosition):
                pixels[x] = (0, 0, 40)
                sleep(0.05)
                
        #wait to show how far on the wheel we are    
        sleep(3)



        # Light Display
        lightCurrent = readLight()
        lightMax = 200
        lightMin = 0
        
        print("The current light level is ", lightCurrent, ". Threshold level is ", lightMax)
        ledPosition = translate(lightCurrent,lightMin,lightMax,1,18)
        print("Light is at ", ledPosition, " out of 18 on the wheel")
        print("")
        
        #clear all neopixels
        pixels.fill((0, 0, 0))    

        # Yellow smiley face if light threshold reached
        if lightCurrent > lightMax:
            pixels.fill((10, 10, 0))
            sleep(0.1)
            pixels[0] = (40, 40, 20)
            pixels[1] = (40, 40, 20)
            pixels[2] = (40, 40, 20)
            pixels[17] = (40, 40, 20)
            pixels[16] = (40, 40, 20)
            pixels[15] = (40, 40, 20)
            pixels[6] = (40, 40, 20)
            pixels[12] = (40, 40, 20)
                        
        elif lightCurrent < lightMax:
            
            #Yellow and white lights LED effect wheel
            for x in range(ledPosition):
                pixels[x] = (40, 40, 20)
                sleep(0.05)
                
            for x in range(ledPosition):
                pixels[x] = (40, 40, 0)
                sleep(0.05)
                
        #wait to show how far on the wheel we are    
        sleep(3)
                
                
                
        # Main Logic and Music Code
        
        """
        Why did I do this code block? I can't remember. 
        # Iterates up to ten before resetting 
        checkHumidityOnlyEvery10Times +=1
         
         # When it gets to ten
        if checkHumidityOnlyEvery10Times % 10 == 0:
        
        Ugg if I delete this I have to unindent everything
        
        Meh. I'll just but an if True so I don't have to.
        """
        
        if True:
             
             # Check the humidity is nice and high
             if get_humidity() > humidityMax:
                
                # reset the humidty counter from 10 back to 0
                checkHumidityOnlyEvery10Times = 0
                
                # Check the light sensor on GPIO 4. "0" means light detected.
                if readLight() > lightMax:
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
                else:
                    
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
    pixels.fill((0, 0, 0))
    GPIO.cleanup()
    mixer.music.stop()
    