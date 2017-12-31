#This code is just for educational use. It shows a Graphical Interface that you could use to control an arm but has no
# code to actually run the servos. See the "Arm_GUI" code for the working version of this.

import sys
import os
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

def outputs(): #outputs servo values to the shell to show current arm position
        print (slider_1.get(), slider_2.get(), slider_3.get(), slider_4.get())
        


mGui = Tk()  #starts TKinter

mGui.geometry("450x800+300+300")  #sets the size of the window


#Window Title

mGui.title("Robo Control v0.1")

#image

img = ImageTk.PhotoImage(Image.open("ez.png"))
panel = Label(mGui, image = img)
panel.pack(side = "top", fill = "both", expand = "no")


#Background
mGui.configure(background='orange')

#slider1

label1= Label(mGui,text="Choose your values using the sliders below").pack()
label2= Label(mGui,text="").pack()
#slider1 Rotation
label= Label(mGui,text="Rotation").pack()
slider_1 = Scale(mGui, orient=HORIZONTAL, from_=150, to=600)
slider_1.pack()

#slider2 BigArm
label2= Label(mGui,text="").pack()
label3= Label(mGui,text="Big Arm").pack()
slider_2 = Scale(mGui, orient=HORIZONTAL, from_=150, to=600)
slider_2.pack()

#slider3 Small Arm
label4= Label(mGui,text="").pack()
label5= Label(mGui,text="Small Arm").pack()
slider_3 = Scale(mGui, orient=HORIZONTAL, from_=150, to=600)
slider_3.pack()

#slider4 Claw
label6= Label(mGui,text="").pack()
label7= Label(mGui,text="Claw").pack()
slider_4 = Scale(mGui, orient=HORIZONTAL, from_=150, to=600)
slider_4.pack()

#button to shows values
label8= Label(mGui,text="").pack()
mbutton = Button(text="Show current values in shell",command = outputs, cursor="dotbox")
mbutton.pack()



#button to quit
label8= Label(mGui,text="").pack()
mbutton2 = Button(text="Exit",command = sys.exit, cursor="pirate")
mbutton2.pack()

mGui.mainloop()

