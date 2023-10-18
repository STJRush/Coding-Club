import datetime
import time
from PCA9685 import PCA9685
from time import ctime 

from time import sleep

print("start")

pwm = PCA9685(0x40)
pwm.setPWMFreq(50)

while True:
    #put word to make time
    timedata = datetime.datetime.now()


    #word reacts to string 
    stringTime = str(timedata)


    #cut out the middle bit and call it justTime
    justTime = stringTime[11:16]


    #time is printed 
    print('the time is ' + justTime)


    #replace : with nothing 
    time=justTime.replace(':', '')

    print(time)
    sleep(10) #only check each minute

    time=int(time)

    def monday():
        
      print("It's Monday")
      print("Mr. Murray should be...")
        
      if time >= 845 and time <= 945:
        print("R11 Period 1")
        pwm.setServoPulse(0,1200)
        
      elif time >= 845 and time <= 945:
        print("R11 Period 2")
        pwm.setServoPulse(0,1200)
        
      elif time >= 1045 and time <= 1100:
        print("On Break!")
        pwm.setServoPulse(0,800)
        
      elif time >= 1100 and time <= 1200:
        print("On Call Period 3")
        pwm.setServoPulse(0,600)

      elif time >= 1200 and time <= 1300:
        print("ICT Support Period 4")
        pwm.setServoPulse(0,2400)

      elif time >= 1300 and time <= 1335:
        print("On Lunch!")
        pwm.setServoPulse(0,1900)
        
      elif time >= 1335 and time <= 1435:
        print("R39 Period 5")
        pwm.setServoPulse(0,300)
        
      elif time >= 1435 and time <= 1535:
        print("R11 Period 6")
        pwm.setServoPulse(0,1200)
        
      elif time >= 1535:
        print("Gone home")
        pwm.setServoPulse(0,1500)
        
      else:
        print("I have no idea. Gone home?")
        pwm.setServoPulse(0,1500)





    def tuesday():
        
      print("It's Tuesday")
      
      if time >= 845 and time <= 940:
        print("R11")
        pwm.setServoPulse(0,1200)
        
      elif time >= 945 and time <= 1045:
        print("Free to annoy")
        pwm.setServoPulse(0,2200)
        
      elif time >= 1045 and time <= 1100:
        print("On Duty")
        pwm.setServoPulse(0,2100)

      elif time >= 1100 and time <= 1200:
        print("R11")
        pwm.setServoPulse(0,1200)
        
      elif time >= 1200 and time <= 1300:
        print("ICT Support")
        pwm.setServoPulse(0,2600)

      elif time >= 1300 and time <= 1335:
        print("On Duty!")
        pwm.setServoPulse(0,2100)

      elif time >= 1335 and time <= 1435:
        print("Free to annoy")
        pwm.setServoPulse(0,2200)

      elif time >= 1435 and time <= 1535:
        print("R11")
        pwm.setServoPulse(0,1200)
        
      else:
        print("I have no idea. Gone home?")
        pwm.setServoPulse(0,1500)


        
        
    def wednesday():
        
        
      print("It's Wednesday")
      
      if time >= 845 and time <= 9400:
        print("R11")
        pwm.setServoPulse(0,1200)
        
      elif time >= 945 and time <= 1045:
        print("On Call")
        pwm.setServoPulse(0,600)

      elif time >= 1045 and time <= 1100:
        print("On Break!")
        pwm.setServoPulse(0,800)
        
      elif time >= 1100 and time <= 1200:
        print("R11")
        pwm.setServoPulse(0,1200)
        
      elif time >= 1200 and time <= 1300:
        print("R39")
        pwm.setServoPulse(0,300)
        
      elif time >= 1300 and time <= 1335:
        print("On Lunch!")
        pwm.setServoPulse(0,1900)
        
      elif time >= 1335 and time <= 1435:
        print("R11")
        pwm.setServoPulse(0,1200)
        
      elif time >= 1435 and time <= 1535:
        print("R39")
        pwm.setServoPulse(0,300)

      else:
        print("I have no idea. Gone home?")
        pwm.setServoPulse(0,1500)


    def thursday():
    
      print("It's Thursday")
       
      if time >= 845 and time <= 9400:
        print("R11")
        pwm.setServoPulse(0,1200)
        
      elif time >= 945 and time <= 1045:
        print("R11")
        pwm.setServoPulse(0,1200)
        
      elif time >= 1045 and time <= 1100:
        print("On Break!")
        pwm.setServoPulse(0,800)
        
      elif time >= 1100 and time <= 1200:
        print("ICT Supportt")
        pwm.setServoPulse(0,2400)

      elif time >= 1200 and time <= 1300:
        print("R11")
        pwm.setServoPulse(0,1200)
        
      elif time >= 1300 and time <= 1335:
        print("On Lunch!")
        pwm.setServoPulse(0,1900)
        
      elif time >= 1335 and time <= 1435:
        print("R11")
        pwm.setServoPulse(0,1200)
        
      elif time >= 1435 and time <= 1535:
        print("R11")
        pwm.setServoPulse(0,1200)
        
      else:
        print("I have no idea. Gone home?")
        pwm.setServoPulse(0,1500)




    def friday():
    
      print("It's Friday")
        
      if time >= 845 and time <= 9400:
        print("R11")
        pwm.setServoPulse(0,1200)
        
      elif time >= 945 and time <= 1045:
        print("R39")
        pwm.setServoPulse(0,300)
        
      elif time >= 1045 and time <= 1100:
        print("On Break!")
        pwm.setServoPulse(0,800)
        
      elif time >= 1100 and time <= 1200:
        print("On Call")
        pwm.setServoPulse(0,600)

      elif time >= 1200 and time <= 1300:
        print("R39")
        pwm.setServoPulse(0,300)
        
      elif time >= 1300 and time <= 1335:
        print("Going home.")
        pwm.setServoPulse(0,1500)

      else:
        print("I have no idea. Gone home?")
        pwm.setServoPulse(0,1500)

    import datetime

    #put word to make time
    timedata = datetime.datetime.now()
    print (timedata)


    day=timedata.weekday()
    print ("Day", day, "of 7")


    #placeholder for Nicky to get day in here


    if day == 0:
      monday()

    elif day == 1:
      tuesday() 
    elif day == 2:
        wednesday()
    elif day == 3:
        thursday()
    elif day == 4:
        friday()
    else:
      pass
      #print('go home hes not here!!!!')
      pwm.setServoPulse(0,1500)

