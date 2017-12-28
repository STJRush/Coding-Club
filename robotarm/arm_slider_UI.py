from __future__ import division

import sys
import os
from Tkinter import *

#import PIL         """Pics are not wokring in 2.7 so this is blocked out"""
#from Tkinter import messagebox
#from PIL import ImageTk , Image


import time

# Import the PCA9685 module.
import Adafruit_PCA9685

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

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


#outputs servo values to the shell to show current arm position
def outputs(): 
        print (slider_1.get(), slider_2.get(), slider_3.get(), slider_4.get())
        pwm.set_pwm(0, 0, slider_1.get())
        pwm.set_pwm(1, 0, slider_2.get())
        pwm.set_pwm(2, 0, slider_3.get())
        pwm.set_pwm(3, 0, slider_4.get())
        




mGui = Tk()  #starts TKinter. TKinter is what makes menus and buttons.



"""
#This line "mGui.geometry" below sets the size of the window.
#Eg. 600 x 800 pixels
#Removing this code shrinks the window to whatever sits inside it.
#For that reason, We're not using it and the window is a snug fit.
"""

#mGui.geometry("600x800+300+300")




#Window Title. You'll see this text in the title of the window.

mGui.title("Robo Control v0.5")




#image WASN'T WORKING in RASPIAN SO THIS CODE COMMENT BLOCKED OUT

"""
img = ImageTk.PhotoImage(Image.open("/home/pi/Desktop/ez.png"))
panel = Label(mGui, image = img)
panel.pack(side = "top", fill = "both", expand = "no")
"""

#Background and colour. You can set it to common colour names or hex codes.
mGui.configure(background='orange')



#slider1

label1= Label(mGui,text="Choose your values using the sliders below").pack()
label2= Label(mGui,text="").pack()

#slider1 Rotation
label= Label(mGui,text="Rotation").pack() #The name of the slider that appears beside it.
slider_1 = Scale(mGui, orient=HORIZONTAL, from_=150, to=600)
slider_1.set(300) #Sets the starting position of the arm to this value
slider_1.pack()

#slider2 BigArm
label2= Label(mGui,text="").pack() #blank label to space things out a bit.
label3= Label(mGui,text="Big Arm").pack() #The name of the slider that appears beside it.
slider_2 = Scale(mGui, orient=HORIZONTAL, from_=150, to=600)
slider_2.set(300) #Sets the starting position of the arm to this value
slider_2.pack()

#slider3 Small Arm
label4= Label(mGui,text="").pack() #blank label to space things out a bit.
label5= Label(mGui,text="Small Arm").pack() #The name of the slider that appears beside it.
slider_3 = Scale(mGui, orient=HORIZONTAL, from_=150, to=600)
slider_3.set(300) #Sets the starting position of the arm to this value
slider_3.pack()

#slider4 Claw
label6= Label(mGui,text="").pack() #blank label to space things out a bit.
label7= Label(mGui,text="Claw").pack() #The name of the slider that appears beside it.
slider_4 = Scale(mGui, orient=HORIZONTAL, from_=150, to=600)
slider_4.set(300) #Sets the starting position of the arm to this value
slider_4.pack()

#button to shows values
label8= Label(mGui,text="").pack() #blank label to space things out a bit.
mbutton = Button(text="Move arm",command = outputs, cursor="dotbox")
mbutton.pack()



#button to quit
label9= Label(mGui,text="").pack()
mbutton2 = Button(text="Exit",command = sys.exit, cursor="pirate")
mbutton2.pack()

mGui.mainloop()

############################################
#OLD CODE FOR TEXT BASED CONTROL
#Mr Murray's Custom code starts here

#Small arm cannot exceed 340 without breaking the arm
"""
ROTATION = 300
BIGARM = 300
SMALLARM = 300
CLAW = 300


pwm.set_pwm(0, 0, slider_1.get())   




print("The arm is set to ROTATION" + str(ROTATION) +" BIGARM"+ str(BIGARM)+" SMALLARM"+str(SMALLARM)+str(CLAW)+" CLAW")

print("Enter a value from 150 to 600")

ROTATION=int(raw_input("Type in number for ROTAION of whole arm")) #these take the instructions from the user
BIGARM=int(raw_input("Type in number for reach of the big BIGARM"))
SMALLARM=int(raw_input("Type in number for the cooping up SMALLARM"))
CLAW=int(raw_input("Type in number for the CLAW grip"))

pwm.set_pwm(0, 0, ROTATION) #these 3 lines send the users three values to the arm
pwm.set_pwm(1, 0, BIGARM)
pwm.set_pwm(2, 0, SMALLARM)
pwm.set_pwm(3, 0, CLAW)  #200 is claw open xgz is claw closed

#WARNING: Just because a servo can move to a position doesn't mean that the arm can do so without breaking.

###################################################

"""


