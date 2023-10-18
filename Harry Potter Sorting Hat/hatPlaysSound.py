
import RPi.GPIO as GPIO #GPIO Libraries
from time import sleep #Sleep Functions
import time
import os
import random

GPIO.setmode(GPIO.BCM) #Setting Up
GPIO.setup(18, GPIO.IN) #input from microbit

#os.system('mplayer music1.mp3 &')
sleep(3)

#plays an intro phrase at random

introNumber = random.randint(1, 4)
print(introNumber)

if introNumber==1:
    print("PLAYING INTRO 1")
    os.system('mplayer comeforward.wav')
    
elif introNumber==2:
    print("PLAYING INTRO 2")
    os.system('mplayer andyou.wav')
    
elif introNumber==3:
    print("PLAYING INTRO 3")
    os.system('mplayer comecloser.wav')

elif introNumber==4:
    print("PLAYING INTRO 4")
    os.system('mplayer cantseeyou.wav')

elif introNumber==5:
    print("PLAYING INTRO 4")
    os.system('mplayer spareme.wav')


play = 0  #starts off not playing audio


#plays a house name when hat is shaken

while True:

  if GPIO.input(18)==0:  #no signal detected from Micro:bit
    print("No sound yet...")
    print("Waiting for a hat shake....")
    sleep(0.2)


  elif GPIO.input(18)==1 and play == 1:
    print("Already playing. Relax!")

  elif GPIO.input(18)==1 and play == 0:  #signal detected
    print("PLAYING")
    songNumber = random.randint(1, 10)
    print(songNumber)

    if songNumber == 1:  
        os.system('mplayer andyou.wav')
    elif songNumber == 2:  
        os.system('mplayer cantseeyou.wav')
    elif songNumber == 3:  
        os.system('mplayer grif1.wav')
        os.system('mplayer cheer1.wav')
    elif songNumber == 4:  
        os.system('mplayer grif2.wav')
        os.system('mplayer cheer2.wav')
    elif songNumber == 5:  
        os.system('mplayer grif3.wav')
    elif songNumber == 6:  
        os.system('mplayer huf1.wav')
        os.system('mplayer yay.mp3')
    elif songNumber == 7:  
        os.system('mplayer slith1.wav')
        os.system('mplayer yay.mp3')
    elif songNumber == 8:  
        os.system('mplayer veryhonorable.wav')
    elif songNumber == 9:  
        os.system('mplayer what.wav')
    

    else:
        print("errrores")
        os.system('mplayer what.wav &')
      
    play = 1 #now playing
    sleep(5)
    play = 0




