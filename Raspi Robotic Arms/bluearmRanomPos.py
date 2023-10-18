import time
from PCA9685 import PCA9685
from time import ctime
import random
import os


print("start")

pwm = PCA9685(0x40)
pwm.setPWMFreq(50)



pwm.setServoPulse(0,1500) # starts at 300 to 2600... 1500is about middle

def pointInRandomDirection():
    randomDirectionValue=random.randint(1,2600)
    print("Direction Value:", randomDirectionValue)
    pwm.setServoPulse(0,randomDirectionValue)
    
    
    randomTimeValue=random.randint(1,15)
    print("moving in ", randomTimeValue, "seconds")
    #time.sleep(randomTimeValue)
    
    
    
    for x in range(randomTimeValue):
        time.sleep(1)
        os.system('mplayer pings.wav')
        
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
                    randsound()
            
            except:
                pass
            
        elif choice == "2":
            print("Shooting water")
            os.system('mplayer target.wav')
            os.system('mplayer alarm.wav')
            
            
        elif choice == "3":
            print("exiting program")
            pwm.setServoPulse(0,1500) #return to start position
            os.system('mplayer shutdown.wav')
            os.system('mplayer goodnight.wav')
            return 0
            break

#os.system('mplayer activated.wav')



def randsound():
        
    randomSoundNumber=random.randint(1,10)

    if randomSoundNumber == 1:
        os.system('mplayer haloo.wav')
    elif randomSoundNumber == 2:
        os.system('mplayer anyonethere.wav')
    elif randomSoundNumber == 3:
        os.system('mplayer come.wav')
    elif randomSoundNumber == 4:
        os.system('mplayer search.wav')
    elif randomSoundNumber == 5:
        os.system('mplayer canvas.wav')
    elif randomSoundNumber == 6:
        os.system('mplayer friend.wav')
    elif randomSoundNumber == 7:
        os.system('mplayer hi.wav')
    elif randomSoundNumber == 8:
        os.system('mplayer stillthere.wav')
    elif randomSoundNumber == 9:
        os.system('mplayer whosthere.wav') 
    else:
        print("Error playing sound")

os.system('mplayer turnon.wav')
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

            #EGG
