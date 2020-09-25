
#pings a bunch of switches or whatever to see if the internet is working. The command line was sad so I added some colour.

pingTargets = ["10.1.199.09","10.1.199.10","10.1.199.11", "10.1.199.12", "10.1.199.13", "10.1.199.14"]


from ping3 import ping, verbose_ping
from pygame import mixer
from time import sleep
import colorama
from colorama import init
init()
from colorama import Fore, Back, Style

severityLevel = 10

# Starting the mixer
mixer.init()

# Loading the songs and sounds
mixer.music.load("birds.mp3")
#crash_sound = mixer.Sound("crash.mp3")
#soundy = mixer.Sound("malf.wav")
#mixer.Sound.play(soundy)

# Setting the volume
mixer.music.set_volume(0.7)

# Start playing the song
mixer.music.play()


"""print(Fore.RED + 'some red text')
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
sleep(3)


print("This program will ping these targets:")
print(pingTargets)
print("You can add to the list of targets by editing the first line of this .py file in notepad")
print(Fore.BLACK + Back.GREEN + "Nice nature sounds means good network weather")
sleep(2)
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
mixer.music.stop()

print("The colour will change too if things get bad.")
print("The idea is that you don't have to keep looking at the screen to know how the network is doing")

try:

    while True:

        for x in range(len(pingTargets)):

            ip = pingTargets[x]

            print(Back.WHITE +"Target", x+1)
            val = verbose_ping(ip, interval=0.5, count = 3)



            if ping(ip) == None:
                print(Fore.RED + Back.BLACK + "WARNING! ENTIRE SWITCH IS DOWN!")
                #mixer.Sound.play(malf_sound)
                print(Style.RESET_ALL)

            else:
                
                try:  #this is because sometimes it wasn't working
                 snapshot=ping(ip)*1000
                except:
                 snapshot = 42 #this is my favorite number
                 print("Oooops")


                if snapshot < 10:
                    print(Fore.BLACK + Back.GREEN + "We're all good")
                    
                    if severityLevel != 0:
                    
                        print("Everyone take a breather")
                        mixer.music.stop()
                        mixer.music.load("birds.mp3")
                        mixer.music.play()
                    
                    
                    sleep(1)
                    
                    severityLevel = 0

                elif snapshot > 10 and snapshot < 100:
                    print(Fore.BLACK + Back.YELLOW + "Could be better")
                    
                    if severityLevel != 1:
                    
                        mixer.music.stop()
                        mixer.music.load("drizzle.mp3")
                        mixer.music.play()
                    
                    sleep(1)
                    
                    severityLevel = 1

                elif snapshot > 100 and snapshot < 500:
                    print(Fore.BLACK + Back.RED + "Not great, not terrible")
                   
                    if severityLevel != 2:
                    
                        mixer.music.stop()
                        mixer.music.load("rain.mp3")
                        mixer.music.play()
                    
                    sleep(1)
                    
                    severityLevel = 2

                elif snapshot > 500 and snapshot < 1000:
                    print(Fore.WHITE + Back.RED + "PANIC PANIC PANIC")
                    mixer.music.stop()
                    mixer.music.load("jaziswind.mp3")
                    mixer.music.play()
                    sleep(1)
                    
                   


                elif snapshot > 1000:
                    print("ALARM ALARM")
                    print(Fore.WHITE + Back.RED + "IT'S HAPPENING AGAIN!")
                    print(Fore.WHITE + Back.RED + "RUN FOR YOUR LIVES!")
                    #mixer.Sound.play(crash_sound)
                    
                    


                else:
                    print("WHAT KINDA PING IS THAT?")

                print("Ping is about ", snapshot)

                print(Style.RESET_ALL)

except KeyboardInterrupt:
    print(Style.RESET_ALL)
    print("Goodbye")


