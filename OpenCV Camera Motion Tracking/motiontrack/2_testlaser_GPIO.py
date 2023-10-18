#For testing if GPIOs are working
#Godspeed.

import RPi.GPIO as GPIO   #lets you use GPIO
from time import sleep    #lets you use sleep(2) as a timer for the lights

GPIO.setmode(GPIO.BCM)    #tells the program what labeling system to use

GPIO.setup(14, GPIO.OUT)  #tells the pi exactly what number pin you'll be using


print("Testing GPIO14")



print("GPIOTEST14 ON")
GPIO.output(14, GPIO.HIGH)     #tells the pi to turn on this pin
sleep(1)
print("GPIOTEST14 OFF")        #waits 2 seconds
GPIO.output(14, GPIO.LOW)      #tells the pi to turn off this pin

sleep(0.2)

#the cleanup

GPIO.cleanup()             #shuts down all GPIO stuff