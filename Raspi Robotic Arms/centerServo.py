# This program makes a pan tilt servo setup look about

import time
from PCA9685 import PCA9685
from time import ctime 


print("start")

pwm = PCA9685(0x40)
pwm.setPWMFreq(50)

def center():
    pwm.setServoPulse(0,1300) 
    time.sleep(1)
    pwm.setServoPulse(1,1300)
    time.sleep(1)
    
def lookLeft():
    pwm.setServoPulse(0,1000) 
    time.sleep(1)
    
def lookRight():
    pwm.setServoPulse(0,1600) 
    time.sleep(1)
    
def lookUp():
    pwm.setServoPulse(1,1000) 
    time.sleep(1)

def lookDown():
    pwm.setServoPulse(1,1600) 
    time.sleep(1)

#look about
time.sleep(1)

center()

lookLeft()
lookUp()
lookDown()

lookRight()
lookUp()
lookDown()


center()
#gpio.cleanup()

print("done")

            


