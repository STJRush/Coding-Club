# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

print('Moving servo on channel 0, press Ctrl-C to quit...')
############################################
#Mr Murray's Custom code starts here

#Small arm cannot exceed 340 without breaking the arm

ROTATION = 300
BIGARM = 300
SMALLARM = 300

while True:


    print("The arm is set to ROTATION" + str(ROTATION) +" BIGARM"+ str(BIGARM)+" SMALLARM"+str(SMALLARM))
    
    print("Enter a value from 150 to 600")

    ROTATION=int(raw_input("Type in number for ROTAION of whole arm")) #these take the instructions from the user
    BIGARM=int(raw_input("Type in number for reach of the big BIGARM"))
    SMALLARM=int(raw_input("Type in number for the cooping up SMALLARM"))
    
    pwm.set_pwm(0, 0, ROTATION) #these 3 lines send the users three values to the arm
    pwm.set_pwm(1, 0, BIGARM)
    pwm.set_pwm(2, 0, SMALLARM)

    #WARNING: Just because a servo can move to a position doesn't mean that the arm can do so without breaking.
    
###################################################
""" blocked off original code
while True:
    # Move servo on channel O between extremes.
    pwm.set_pwm(0, 0, servo_min)
    time.sleep(1)
    pwm.set_pwm(0, 0, servo_max)
    time.sleep(1)
"""
