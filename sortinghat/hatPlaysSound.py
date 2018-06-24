
import RPi.GPIO as GPIO #GPIO Libraries
from time import sleep #Sleep Functions
import time
import os

GPIO.setmode(GPIO.BCM) #Setting Up
GPIO.setup(21, GPIO.IN) #input from microbit


def microCheck():
    play = 0  #starts off not playing audio
    while True:

      if GPIO.input(21)==0:  #no signal detected from Micro:bit
        print("No sound yet...")
        sleep(0.2)
        
        

      elif GPIO.input(21)==1 and play == 0:  #signal detected
        print("PLAYING")  
        os.system('mplayer test.wav &')
        play = 1 #now playing
        sleep(10)
        play = 0
        
      else:
          print("Already playing. Relax!")

print("Staring program")

microCheck()



