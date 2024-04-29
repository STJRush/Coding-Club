# Load Cell Weight Scales Simple Test

import RPi.GPIO as GPIO
import time
import sys
from hx711 import HX711


#This function just cleans up when everything is done.
def cleanAndExit():
    print "Cleaning..."
    GPIO.cleanup()
    print "Bye!"
    sys.exit()

#Using GPIO 5,6 for the scale.
hx = HX711(5, 6)
hx.set_reading_format("LSB", "MSB")
hx.set_reference_unit(412)

hx.reset()
hx.tare()



print("Welcome to Mr. Murray's Cookie Scale")

print(" me no care   (.)(*)            ")
print("       ...   / ___, \  .-.      ")
print("       .-. _ \ '--' / (:::)     ")
print("      (:::{ \-`--=-`-/ }^       ")
print("       `-' ` /      \ `         ")
print("             \      /           ")
print(" long as    _/  /\  \_          ")
print(" me get    {   /  \   }         ")
print(" cookie     `-`    `-`           ")


while True:
    
    try:
        
        val = hx.get_weight(5)
        print (str(val)+"g worth of delicious cookie detected")
        

        hx.power_down()
        hx.power_up()
        time.sleep(0.5)   #this pause can be bigger if you're having errors

    except:
      print("Me get errors")


