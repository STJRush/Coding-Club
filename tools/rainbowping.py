from ping3 import ping, verbose_ping

from colorama import init
init()
import colorama
from colorama import Fore, Back, Style

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

try:

    while True:
        print(Back.MAGENTA +"Target 1")
        verbose_ping('192.168.8.100', interval=0.5, count = 3)

        print("")

        print(Back.BLUE + "Target 2")
        verbose_ping('192.168.8.100', interval=0.5, count = 3)

        print("")

        print(Back.CYAN + "Target 3")
        verbose_ping('192.168.8.100', interval=0.5, count = 3)

        print("")

        print(Back.GREEN + "Target 4")
        verbose_ping('192.168.8.100', interval=0.5, count = 3)

        print("")

        print(Back.YELLOW + "Target 5")
        verbose_ping('192.168.8.100', interval=0.5, count = 3)

        print("")

        print(Back.RED + "Target 6")
        verbose_ping('192.168.8.100', interval=0.5, count = 3)

        print(Style.RESET_ALL)
        
        print("")
        print("")
        print("")

except KeyboardInterrupt:
    print(Style.RESET_ALL)
    print("Goodbye")


