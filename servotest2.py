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

"""I've blocked out this code from the Adafruit stock example
print('Moving servo on channel 0, press Ctrl-C to quit...')
while True:
    # Move servo on channel O between extremes.
    pwm.set_pwm(0, 0, servo_min)
    time.sleep(1)
    pwm.set_pwm(0, 0, servo_max)
    time.sleep(1)
"""




####MR. MURRAY'S CODE STARTS HERE####
"""
The code to run a servo is just this one line:
"""

#pwm.set_pwm(0, 0, 300)

"""
WHAT THIS MEANS:

pwm.set_pwm([channel number goes here], 0, [servo direction number goes here])
eg.

The servo function has three parameters seperated by commas.

(0,0,0)

Change the first 0 to select what servo you want to use.

eg. (1,0.0) selects servo plugged into in channel 1 on the servo board.


I have no idea what the second parameter is or does.


Change the third parameter to any value from 150 to 600 to control servos's direction.

eg.
pwm.set_pwm(0, 0, 300) sets servo plugged into channel 0 to about half way.

pwm.set_pwm(2, 0, 150) sets servo plugged into channel 2 to all the way left.

pwm.set_pwm(1, 0, 600) sets servo plugged into channel 1 to all the way right.


"""
#YOUR CODE STARTS HERE

pwm.set_pwm(0, 0, 150) #sets the servo in channel 0 to about half way.
