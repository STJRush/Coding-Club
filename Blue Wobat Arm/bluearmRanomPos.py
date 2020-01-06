import time
from PCA9685 import PCA9685
from time import ctime
import random
import os


print("start")

pwm = PCA9685(0x40)
pwm.setPWMFreq(50)



pwm.setServoPulse(0,300) # starts at 300 to 2600... 1500is about middle

def pointInRandomDirection():
    randomDirectionValue=random.randint(1,2600)
    print("Direction Value:", randomDirectionValue)
    pwm.setServoPulse(0,randomDirectionValue)
    
    
    randomTimeValue=random.randint(1,30)
    print("moving in ", randomTimeValue, "seconds")
    time.sleep(randomTimeValue)
    pwm.setServoPulse(0,randomDirectionValue)
    



def mainMenu():
    
    while True:
        print("1: Scan area")
        
        print("2: Shoot Water Test")
        
        print("3: End program")
        
        
        choice = input("Type 1, 2 or 3 and hit return")
        
        if choice == "1":
            print("starting scan")
            os.system('mplayer haloo.wav')
            
            
            print("Use ctrl + C to return to the main menu")
            
            
            
            try:
                while True:
                    pointInRandomDirection()
            
            except:
                pass
            
        elif choice == "2":
            print("Shooting water")
            
        elif choice == "3":
            print("exiting program")
            
            return 0
            break

#os.system('mplayer activated.wav')

            
mainMenu()    
"""
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
"""

time.sleep(1)

#gpio.cleanup()

print("done")

            

