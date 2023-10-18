
# Beat timer twitch reaction speed max thunder low latency megaflop code

# DOES NOT DISPLAY CORRECTLY IN REPL, USE THONNY

from time import sleep
beatTimer = 0

print("Press CTRL+C near 5 for MAX POWER!")
while True:
    
    try:
        for x in range(10):
          print("-" end = "")
          sleep(0.07)
          beatTimer = beatTimer + 1
          print(beatTimer, end = "")
          
        #reset timer
        beatTimer = 0
        
        #clear screen
        print("\033[H\033[J")
      
    except KeyboardInterrupt:
        print("You stopped the timer at", beatTimer)
        break

if (beatTimer >= 0 and beatTimer <= 3) or (beatTimer >= 7 and beatTimer <= 10):
    print("Weak effort! Low Power")
elif (beatTimer == 4 or beatTimer == 6):
    print("High power shot! Nice work!")
elif (beatTimer == 5):
    print("PERFECT!")

  
  
