import time
from PCA9685 import PCA9685
from time import ctime 


print("start")

pwm = PCA9685(0x40)
pwm.setPWMFreq(50)

'''
for i in range(300,800):
    pwm.setServoPulse(0,i) # starts at 300 to 2600... 1500is about middle
    time.sleep(0.1)
    print(i)
'''  

pwm.setServoPulse(0,300) # starts at 300 to 2600... 1500is about middle


time.sleep(1)
pwm.setServoPulse(0,600) 
time.sleep(1)
pwm.setServoPulse(0,900) 
time.sleep(1)
pwm.setServoPulse(0,1200) 
time.sleep(1)
pwm.setServoPulse(0,1500) 
time.sleep(1)

pwm.setServoPulse(0,1800) 
time.sleep(1)
pwm.setServoPulse(0,2100) 
time.sleep(1)
pwm.setServoPulse(0,2400)
time.sleep(1)
pwm.setServoPulse(0,2600)


time.sleep(1)

#gpio.cleanup()

print("done")

            

