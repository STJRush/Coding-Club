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
        



def resetArmPosition(): 
        print ("Reset arm position to ", 300, 300, 300, 300)
        pwm.set_pwm(0, 0, 300)
        pwm.set_pwm(1, 0, 300)
        pwm.set_pwm(2, 0, 300)
        pwm.set_pwm(3, 0, 300)

        slider_1.set(300)
        slider_2.set(300)
        slider_3.set(300)
        slider_4.set(300)
        


#outputs servo values to the shell then runs a sequence
def runSequence():


        print ("Starting Position", slider_1.get(), slider_2.get(), slider_3.get(), slider_4.get())

        #position 1 in sequence of moves
        

        
        slider_1.set(r1)
        slider_2.set(b1)
        slider_3.set(s1)
        slider_4.set(c1)

        print ("Position 1",r1, b1, s1, c1)

        pwm.set_pwm(0, 0, r1)
        pwm.set_pwm(1, 0, b1)
        pwm.set_pwm(2, 0, s1)
        pwm.set_pwm(3, 0, c1)
        
        time.sleep(2)

        #position 2 in sequence of moves
        
        slider_1.set(r2)
        slider_2.set(b2)
        slider_3.set(s2)
        slider_4.set(c2)

        print ("Position 2",r2, b2, s2, c2)

        pwm.set_pwm(0, 0, r2)
        pwm.set_pwm(1, 0, b2)
        pwm.set_pwm(2, 0, s2)
        pwm.set_pwm(3, 0, c2)
        
        time.sleep(2)


        #position 3 in sequence of moves
        
        slider_1.set(r3)
        slider_2.set(b3)
        slider_3.set(s3)
        slider_4.set(c3)

        print ("Position 3",r3, b3, s3, c3)

        pwm.set_pwm(0, 0, r3)
        pwm.set_pwm(1, 0, b3)
        pwm.set_pwm(2, 0, s3)
        pwm.set_pwm(3, 0, c3)
        
        time.sleep(2)

         #position 4 in sequence of moves
        
        slider_1.set(r4)
        slider_2.set(b4)
        slider_3.set(s4)
        slider_4.set(c4)

        print ("Position ",r4, b4, s4, c4)

        pwm.set_pwm(0, 0, r4)
        pwm.set_pwm(1, 0, b4)
        pwm.set_pwm(2, 0, s4)
        pwm.set_pwm(3, 0, c4)
        
        time.sleep(2)


#records a sequence
def recordSequence():
    label10= Label(mGui,text="Move sliders now").pack() #blank label to space things out a bit.
    mbuttonA = Button(text="Record First postion",command = recordFirstValue, cursor="dotbox")
    mbuttonA.pack()

def recordFirstValue():
    global r1; r1 = slider_1.get()
    global b1; b1 = slider_2.get()
    global s1; s1 = slider_3.get()
    global c1; c1 = slider_4.get()

    label11= Label(mGui,text=("Postion 1:", slider_1.get(), slider_2.get(), slider_3.get(), slider_4.get())).pack()
    mbuttonA = Button(text="Record second position",command = recordSecondValue, cursor="dotbox")
    mbuttonA.pack()

def recordSecondValue():
    global r2; r2 = slider_1.get()
    global b2; b2 = slider_2.get()
    global s2; s2 = slider_3.get()
    global c2; c2 = slider_4.get()

    label11= Label(mGui,text=("Postion 2:", slider_1.get(), slider_2.get(), slider_3.get(), slider_4.get())).pack()
    mbuttonA = Button(text="Record third position",command = recordThirdValue, cursor="dotbox")
    mbuttonA.pack()

def recordThirdValue():
    global r3; r3 = slider_1.get()
    global b3; b3 = slider_2.get()
    global s3; s3 = slider_3.get()
    global c3; c3 = slider_4.get()

    label11= Label(mGui,text=("Postion 3:", slider_1.get(), slider_2.get(), slider_3.get(), slider_4.get())).pack()
    mbuttonA = Button(text="Record forth position",command = recordForthValue, cursor="dotbox")
    mbuttonA.pack()

def recordForthValue():
    global r4; r4 = slider_1.get()
    global b4; b4 = slider_2.get()
    global s4; s4 = slider_3.get()
    global c4; c4 = slider_4.get()

    label11= Label(mGui,text=("Postion 4:", slider_1.get(), slider_2.get(), slider_3.get(), slider_4.get())).pack()
    label12= Label(mGui,text=("Sequence ready. Click Run Squence")).pack()


    mbuttonA = Button(text="Save to file",command = saveSequenceToFile, cursor="dotbox")
    mbuttonA.pack()

def saveSequenceToFile():
    f = open("armcode.txt", "wb") #opens or creates a text file to write the code to called armcode.txt
    
    f.write("First Position \n")
    f.write( str(r1)+"\n")
    f.write( str(b1)+"\n")
    f.write( str(s1)+"\n")
    f.write( str(c1)+"\n")

    f.write("Second Position \n")
    f.write( str(r2)+"\n")
    f.write( str(b2)+"\n")
    f.write( str(s2)+"\n")
    f.write( str(c2)+"\n")

    f.write("Third Position \n")
    f.write( str(r3)+"\n")
    f.write( str(b3)+"\n")
    f.write( str(s3)+"\n")
    f.write( str(c3)+"\n")

    f.write("Forth Position \n")
    f.write( str(r4)+"\n")
    f.write( str(b4)+"\n")
    f.write( str(s4)+"\n")
    f.write( str(c4)+"\n")


    



    
    f.close
    
    label12= Label(mGui,text=("File saved as: armcode")).pack()


    
#define variables

r1=534
b1=329
s1=400
c1=163

r2=534
b2=329
s2=322
c2=470

r3=300
b3=290
s3=269
c3=470

r4=300
b4=290
s4=269
c4=163

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
#mGui.configure(background='grey')



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




#button to reset arm to starting position
label10= Label(mGui,text="").pack() #blank label to space things out a bit.
mbutton = Button(text="Reset Arm Postion",command = resetArmPosition, cursor="dotbox")
mbutton.pack()

#button to record a program
label10= Label(mGui,text="").pack() #blank label to space things out a bit.
mbutton = Button(text="Record a program",command = recordSequence, cursor="dotbox")
mbutton.pack()

#button to run a sequemce of moves
label9= Label(mGui,text="").pack() #blank label to space things out a bit.
mbutton = Button(text="Run a sequence",command = runSequence, cursor="dotbox")
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

Notes on wiring of claw to servo. 

1 orange to      black to   white
2 red to         blue to    black
3 brown to       green to   brown


###################################################

"""


