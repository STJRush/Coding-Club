import time
from PCA9685 import PCA9685
from time import ctime 


print("start")

pwm = PCA9685(0x40)
pwm.setPWMFreq(50)

pwm.setServoPulse(0,2200) # starts at 300 to 2600... 1500is about middle
pwm.setServoPulse(1,900) # far    less is forward
pwm.setServoPulse(2,1500) # turn
pwm.setServoPulse(3,1500) # claw

time.sleep(1)
'''
pwm.setServoPulse(0,300)
pwm.setServoPulse(1,400)
pwm.setServoPulse(2,400) # turn
pwm.setServoPulse(3,1600) # claw  1600 open 400 closed
'''
#gpio.cleanup()

print("done")

			

