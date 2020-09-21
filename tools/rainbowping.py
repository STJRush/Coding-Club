
#pings a bunch of switches or whatever to see if the internet is working. The command line was sad so I added some colour.

from ping3 import ping, verbose_ping
from pygame import mixer
from time import sleep
import colorama
from colorama import init
init()
from colorama import Fore, Back, Style



# Starting the mixer
mixer.init()

# Loading the songs and sounds
mixer.music.load("birds.mp3")
crash_sound = mixer.Sound("crash.mp3")
malf_sound = mixer.Sound("malf.mp3")

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
pingTargets = ["192.168.8.100", "192.168.8.105", "192.168.8.125"]

print(pingTargets[0])


try:

    while True:

        for x in range(len(pingTargets)):

            ip = pingTargets[x]

            print(Back.WHITE +"Target", x+1)
            val = verbose_ping(ip, interval=0.5, count = 3)



            if ping(ip) == None:
                print(Fore.RED + Back.BLACK + "WARNING! ENTIRE SWITCH IS DOWN!")
                mixer.Sound.play(malf_sound)
                print(Style.RESET_ALL)

            else:
                snapshot=ping(ip)*1000


                if snapshot < 10:
                    print(Fore.BLACK + Back.GREEN + "We're all good")
                    mixer.music.stop()
                    mixer.music.load("birds.mp3")
                    mixer.music.play()
                    sleep(1)

                elif snapshot > 10 and snapshot < 100:
                    print(Fore.BLACK + Back.YELLOW + "Could be better")
                    mixer.music.stop()
                    mixer.music.load("drizzle.mp3")
                    mixer.music.play()
                    sleep(1)

                elif snapshot > 100 and snapshot < 500:
                    print(Fore.BLACK + Back.RED + "Not great, not terrible")
                    mixer.music.stop()
                    mixer.music.load("rain.mp3")
                    mixer.music.play()
                    sleep(1)

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
                    mixer.Sound.play(crash_sound)


                else:
                    print("WHAT KINDA PING IS THAT?")

                print("Ping is about ", snapshot)

                print(Style.RESET_ALL)

except KeyboardInterrupt:
    print(Style.RESET_ALL)
    print("Goodbye")


