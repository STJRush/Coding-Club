import datetime
import time
from PCA9685 import PCA9685
from time import ctime 

from time import sleep

print("start")

pwm = PCA9685(0x40)
pwm.setPWMFreq(50)

while True:
    
    print("START AT R11")
    pwm.setServoPulse(0,1200)
    sleep(2)

    print("R39")
    pwm.setServoPulse(0,300)
    sleep(1.5)

    print("On Call Period 3")
    pwm.setServoPulse(0,600)
    sleep(1.5)
    
    print("On Break!")
    pwm.setServoPulse(0,800)
    sleep(1.5)
    
    print("R11 Period 1")
    pwm.setServoPulse(0,1200)
    sleep(1.5)

    print("Gone home. NO IDEA")
    pwm.setServoPulse(0,1500)
    sleep(1.5)
    
    print("On Lunch!")
    pwm.setServoPulse(0,1900)
    sleep(1.5)
    
    print("Free to annoy")
    pwm.setServoPulse(0,2200)
    sleep(1.5)

