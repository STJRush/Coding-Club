import time
from PCA9685 import PCA9685
from time import ctime 


print("start")

pwm = PCA9685(0x40)
pwm.setPWMFreq(50)


rotation = 1500
claw = 1500
lean_forward = 1500
lift = 1500

pwm.setServoPulse(0,rotation) # starts at 300 to 2600... 1500is about middle
pwm.setServoPulse(1,claw) # starts at 300 to 2600... 1500is about middle
pwm.setServoPulse(2,lift) # starts at 300 to 2600... 1500is about middle
pwm.setServoPulse(3,lean_forward) # starts at 300 to 2600... 1500is about middle



time.sleep(2)


pwm.setServoPulse(0,0) # starts at 300 to 2600... 1500is about middle
pwm.setServoPulse(1,0) # starts at 300 to 2600... 1500is about middle
pwm.setServoPulse(2,0) # starts at 300 to 2600... 1500is about middle
pwm.setServoPulse(3,0) # starts at 300 to 2600... 1500is about middle




#gpio.cleanup()

print("done")

            

