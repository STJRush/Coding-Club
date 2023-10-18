
# pings a bunch of switches or whatever to see if the internet is working. The command line was sad so I added some colour and sound.
# Does internal switch pinging for 10min and then uploads an external speed test result to Thingspeak
# TODO: Run at a certain time as prefab powered off after hours as Libary and Prefab 25 26 Switch seem to go down

# Graph at https://thingspeak.com/channels/1158821

pingTargets = {"Core":"10.1.199.1",
               "Main Coms and Server Room 32F Fibre Out ":"10.1.199.8", #ZYXEL XGS4600-32F
               "Main Coms and Server Room SW1-01 ":"10.1.199.11",
               "Room 39 SW1-02 WiFi Access Points":"10.1.199.12", # ZYXEL GS1920-24HP
               "Office Between Prefab Room 25 and Room 26":"10.1.199.13",
               "R22 Science Lab Beside Preproom":"10.1.199.14", # GS1900-10HP
               "Room 39 SW-V-02 Computer ":"10.1.199.15", # ZYXEL GS1920-24HP
               "Main Coms and Server Room Voice SW-01 ":"10.1.199.16", #ZYXEL GS1900-10HP
               "Room 6 Computer Room Small Voice switch ":"10.1.199.17", # R6 SW-02 ZYXELGS1900-10HP
               "Mystery Big Switch ":"10.1.199.18", # Find Location ZYXEL GS1920-24HP R6?
               "DCG Prefab Room 17":"10.1.199.21", #  SW-SJR-Prefab-01 ZYXEL GS1920-24HP
               "Science Prefab Room 19 ":"10.1.199.22", # SW-SJR-Prefab-02 ZYXEL GS1920-24HP
               "Eimears- Office ":"10.1.199.23", # ZYXEL GS1900-10HP
               "Room 38 Library Small Switch ":"10.1.199.24" #ZYXEL GS1900-10HP FIND LOCATION
               }

# edit Day Time hours
programStartTime = '07:50'
programEndTime = '16:30'

# "I AP WIFI tba":"10.1.199.100" for an example wireless access point



from ping3 import ping, verbose_ping #Speed Test
from pygame import mixer # For sound effects
from time import sleep

import datetime

from logzero import logger, logfile
from pathlib import Path

base_folder = Path(__file__).parent.resolve()
logfile(base_folder/"events.log")

#for thingspeak
import sys
from urllib.request import urlopen

# internet speed test
import speedtest
import statistics

# For pretty text
import colorama
from colorama import init
init()
from colorama import Fore, Back, Style


import pyttsx3 # For spoken voice
engine = pyttsx3.init() 
voices = engine.getProperty('voices')       #getting details of current voice
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
engine.setProperty('voice', voices[1].id)

from random import choice



myAPI = "TKFZ8ENTJ1DPQ3A7"  #your key from your own thingspeak account. Put yours here.

def updateThingSpeak(): 
   print('Now updating external internet speed to thingspeak') 
   baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI    

   f = urlopen(baseURL + "&field1=%s" % (averageExternalInternetSpeed)) 
   print ("Success! I uploaded data point No. ", f.read())
   f.close()


# Starting the mixer
mixer.init()

# Loading the songs and sounds
mixer.music.load("birds.mp3")


crash_sound = mixer.Sound("crashWav.wav")
malf_sound = mixer.Sound("malfWav.wav")

# Setting the volume
mixer.music.set_volume(0.7)

# Start playing the song
mixer.music.play()

listOfExpletives = ["OH NOES!", "OH MY DOG!",
                    "HOLY BROKEN WIFI BATMAN!",
                    "HOLY SHIRT!", "SON OF A PEACH!",
                    "WHAT THE FUDGE!",
                    "DON'T PANIC.",
                    "WE HAVE A SITUATION PEOPLE!",
                    "DID THAT NOISE SOUND BAD? It is bad.",
                    "OH SHAZBOT!",
                    "SON OF A BIT!",
                    "JANEY MACKERS!",
                    "Someone is going to need a hug very soon",
                    "Sorry about this but I've some bad news.",
                    "YOU ARE GOING TO LIKE THIS LIKE A SLAP TO THE FACE",
                    "YOU BETTER MAKES SOME COFFEE. WE HAVE A PROBLEM.",
                    "AH FECK! FECKING HELL!",
                    "YOU PROBABLY DON'T WANT TO HEAR THIS BUT",
                    "HOLY FUDGE CAKES!"]

listOfDeadSwitchIsNowTerms = ["appears to be completely forked. That room and many others will now have no interwebs at all.",
                              "is dead as a dead switch. A dead switch means no dank memes in that room or any rooms near there. An emergancy for sure.",
                    "has gone offline... way way way offline! Like in the way a dead human is offline. Only this is even more sad. ",
                    "is super like dead. Offline like dead. This is not good.",
                              "is no longer online. Someone has broken something somewhere. There will be no internet in that room or connected rooms.",
                              "is offline.",
                              "is not there on the network anymore. I sent a ping to it but got no pong back. Not good. No internet in that room at all now.",
                              "is offline. We've lost the connection to this switch. Everyone in that room will be without interweb until we get this fixed.",
                              "is no longer listed as being online. We've a network issue.",
                              "is showing no connection.",
                              "is not connected to the internet anymore.",
                              "IS DOWN!",
                    "is having a nap. The offline nonresponsive kind of nap. This is not normal. Nothing is normal about this situation. We need to fix that switch.",
                    "has dropped off the radar. Like solid snake from metal gear solid. Hiding in a cardboard box. No internet in there at all. Just like this room and other rooms connected to that switch. ",
                    "has fallen over in the clover. It's dead in the bed. Not good for internets in those rooms. Not good at all.",
                    "is being stupid. Like offline stupid. No internet. No llama memes. Nothing. What will people even do in there without internet?",
                    "is having a bit of a tissy and is no longer online. That is all I know. I also know there is no internet in that room",
                              "is not showing up as online anymore. It was there, now it's not there. You know what else is not there? WiFi in that room now. Not good."]

birdsAreTweeting = False

"""
# Reminder of how to make text coloured and pretty...
print(Fore.RED + 'some red text')
print(Back.GREEN + 'and with a green background')
print(Style.DIM + 'and in dim text')
print(Style.RESET_ALL)
print('back to normal now')
"""

print(Style.BRIGHT + "")

print("              _                 PING?                ")
print("             | |          ___                                       ")
print("             | |===( )   /   |                              ")
print("             |_|   |||  | o o|                                    ")
print("                    ||| ( c  )                  ____         ")
print("                     ||| \= /                  ||   \_         ")
print("                     ||||||                   ||      |        ")
print("                      ||||||                ...||__/|-       ")
print("                      ||||||             __|________|__           ")
print("                        |||             |______________|       ")
print("       Danny's Rainbow  |||             || ||      || ||         ")
print("       Python Pinger    |||             || ||      || ||            ")
print("------------------------|||-------------||-||------||-||-------")
print("                        |__>            || ||      || ||          ")
print("")
print("")
sleep(1)

"""
# Text to speech test
engine.say("Rainbow Ping Test now starting Up")
engine.runAndWait()
engine.stop()
"""

print("This program will ping these targets:")
for key,value in pingTargets.items():
    print(key,"at IP Address", value)
    sleep(0.05)

print("")
print("You can add to the list of targets by editing the first line of this .py file in notepad")
print(Fore.BLACK + Back.GREEN + "Nice nature sounds means good network weather")
sleep(2)

"""
mixer.music.stop()
mixer.music.load("drizzle.mp3")
mixer.music.play()
print(Fore.BLACK + Back.YELLOW + "Drizzle will start if things slow down")
sleep(2)
print(Fore.BLACK + Back.RED + "Then rain if it gets quite slow")
mixer.music.stop()
mixer.music.load("rain.mp3")
mixer.music.play()
sleep(2)
print(Fore.WHITE + Back.RED + "Then a storm if things go to !&££$!")
mixer.music.stop()
mixer.music.load("jaziswind.mp3")
mixer.music.play()
sleep(2)

print("The colour will change too if things get bad.")
print("The idea is that you don't have to keep looking at the screen to know how the network is doing")
print("")
"""



# modified from https://stackoverflow.com/questions/20518122/python-working-out-if-time-now-is-between-two-times



def is_hour_between(start, end):
    
    # Get the time now
    now = datetime.datetime.now().time()
    print("The time now is", now)
    
    # Format the datetime string to just be hours and minutes
    time_format = '%H:%M'
    
    # Convert the start and end datetime to just time
    start = datetime.datetime.strptime(start, time_format).time()
    end = datetime.datetime.strptime(end, time_format).time()

    is_between = False
    is_between |= start <= now <= end
    is_between |= end <= start and (start <= now or now <= end)
    
    return is_between





try:
    
    while True:
        
        #get time
        print(Style.RESET_ALL)
        daytime = is_hour_between(programStartTime, programEndTime) #spans to the next day

        if daytime == True:
            print("It day time hours ", end = "")
        else:
            print("It's after hours ", end = "")
        
        
        #get weekday
        dayNum = int(datetime.datetime.today().weekday()) # get the current day of the week
        print(dayNum)
        
        if dayNum >= 0 and dayNum <= 4:
            print("and it's a weekday.")
        else:
            print("and it's the weekend")
        
        if dayNum >= 0 and dayNum <= 4 and daytime:  # Don't run this on weekends or after hours
            
            print("so we're good to go")
            
            for tests in range(20):

                for key,value in pingTargets.items():

                    ip = value

                    print(Style.BRIGHT+Back.WHITE +"Pinging",key, "over at ", value)
                    val = verbose_ping(ip, interval=0.5, count = 3)
                    print(Style.RESET_ALL)
                    
                    listOfSnappies=[]
                    for x in range(10):
                        snappy = ping(ip)
                        if snappy != None and snappy != False:
                            snappy=round(snappy*1000,1)
                            listOfSnappies.append(snappy)
                            
                        else:
                            print(".", end = ".")
                        
                    if len(listOfSnappies) != 0:
                        avSnappy=statistics.mean(listOfSnappies)
                    else:
                        print("All ping attempts failed. Switch is down")
                        
                        


                    # WHOLE NETWORK SWITCH IS DOWN
                    #print(ping(ip))
                    if len(listOfSnappies) == 0:
                        
                        print(Style.BRIGHT+Fore.WHITE + Back.RED + "WARNING! ENTIRE SWITCH IS DOWN!")
                        mixer.Sound.play(malf_sound)
                        print(Style.RESET_ALL)
                        sleep(3)
                        
                        randomExpletive=choice(listOfExpletives)
                        randomSwitchIsNowTerm=choice(listOfDeadSwitchIsNowTerms)
                        
                        engine.say( randomExpletive+ " " + "..." + key + " " + randomSwitchIsNowTerm)
                        engine.runAndWait()
                        engine.stop()
                        print(randomExpletive+ " " + key + " " + randomSwitchIsNowTerm)
                        sleep(10)
                        
                        # Log this switch being down in the events.log file
                        logger.info(f"Switch Down: "+key+"at IP: "+value)

                    else:
                        # First take a snapshot of ping
                        snapshot=avSnappy

                        # INTERNALLY ALL IS WELL
                        if snapshot < 10:
                            print(Style.BRIGHT+Fore.WHITE + Back.GREEN + "We're all good")
                            
                            if birdsAreTweeting is False:        # if birds are not tweeting, if it's raining...         
                                mixer.music.stop()               # stop the rain. Otherwise let them continue tweeting. Otherwise they'll tweet loop for 2 seconds . Annoying.
                                mixer.music.load("birds.mp3")
                                mixer.music.play()
                                sleep(2)
                            birdsAreTweeting = True # set birds are tweeting flag to TRUE

                        # COULD BE BETTER DRIZZEL
                        elif snapshot > 10 and snapshot < 100:
                            print(Fore.BLACK + Back.YELLOW + "Could be better")
                            mixer.music.stop()
                            mixer.music.load("drizzle.mp3")
                            mixer.music.play()
                            sleep(1)
                            birdsAreTweeting = False

                        elif snapshot > 100 and snapshot < 500:
                            print(Fore.BLACK + Back.RED + "Not great, not terrible")
                            mixer.music.stop()
                            mixer.music.load("rain.mp3")
                            mixer.music.play()
                            sleep(1)
                            birdsAreTweeting = False

                        elif snapshot > 500 and snapshot < 1000:
                            print(Fore.WHITE + Back.RED + "PANIC PANIC PANIC")
                            mixer.music.stop()
                            mixer.music.load("jaziswind.mp3")
                            mixer.music.play()
                            sleep(1)
                            birdsAreTweeting = False


                        elif snapshot > 1000:
                            print("ALARM ALARM")
                            print(Fore.WHITE + Back.RED + "IT'S HAPPENING AGAIN!")
                            print(Fore.WHITE + Back.RED + "RUN FOR YOUR LIVES!")
                            mixer.Sound.play(crash_sound)


                        else:
                            print("WHAT KINDA PING IS THAT?")

                        print("Ping is about ", snapshot)
                        

                        print(Style.RESET_ALL)
        else:
            print("Waiting three hours to not oversaturate thingspeak")
            print("START_____________________________________________FINISH")
            for x in range(50):
                print("-", end = "")
                sleep(200)
                
            print("")

            # External Internet Test
            swanLakePlayingFlag = False
            
        try:
            
            print(Style.BRIGHT+Back.BLUE+Fore.WHITE +"EXTERNAL INTERNET TEST")
            st = speedtest.Speedtest()
            
            listOfTestSpeeds=[]
            for testNo in range(3):
                speedResult = st.download()//1000000 # gets speed in Mbps
                print("Download Speed Test No.",testNo,speedResult,"Mbps")
                listOfTestSpeeds.append(speedResult)

            averageExternalInternetSpeed = round(int(statistics.mean(listOfTestSpeeds)))
            print("----> Average Download speed is", averageExternalInternetSpeed,"Mbps")
            
            if averageExternalInternetSpeed < 50:
                print("The whole internet is really bad")         
            elif averageExternalInternetSpeed < 100:
                print("External internet not great, not terrible.")
            elif averageExternalInternetSpeed > 100 and averageExternalInternetSpeed < 190:
                print("External internet is doing okay ")
            elif averageExternalInternetSpeed > 190:
                print("External internet is doing great! Good internet yay!")
            else:
                print("WTF")
            print("")
            swanLakePlayingFlag = False
            
            updateThingSpeak()
            
        except ValueError:
            print("Internet is completely down")
            sleep(3)
            
            """
            if swanLakePlayingFlag is False:
                mixer.music.load("swanLakeMoscow.mp3")
                mixer.music.play()
                swanLakePlayingFlag = True
            """


except KeyboardInterrupt:
    print(Style.RESET_ALL)
    print("Goodbye")


