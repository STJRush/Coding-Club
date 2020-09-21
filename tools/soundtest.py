from pygame import mixer 
from time import sleep




# Starting the mixer 
mixer.init() 
  
# Loading the song 
mixer.music.load("birds.mp3")
  
# Setting the volume
mixer.music.set_volume(0.7) 
  
# Start playing the song 
mixer.music.play()

crash_sound = mixer.Sound("crash.mp3")

print("doing")
sleep(1)
print("this")
sleep(1)
print("and STOPPING")
mixer.music.stop()
sleep(2)
print("Now playing birds")
sleep(1)
mixer.music.load("birds.mp3")
mixer.music.play()
sleep(1)

sleep(1)
mixer.Sound.play(crash_sound)

# infinite loop
while True:

    print("Press 'p' to pause, 'r' to resume")
    print("Press 'e' to exit the program")
    query = input("  ")

    if query == 'p':

        # Pausing the music
        mixer.music.pause()
    elif query == 'r':

        # Resuming the music
        mixer.music.unpause()
    elif query == 'e':

        # Stop the mixer
        mixer.music.stop()
        break
