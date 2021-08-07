
from pygame import mixer 
from time import sleep
mixer.init() 

# Part 1/3: HOW TO PLAY MUSIC  --------------------------------
mixer.music.load("halo_choir.mp3") # This .mp3 needs to be in the same folder as your .py python file
  
def fade_in_music():
    
    print("Music fading in")
    
    mixer.music.set_volume(0)
    mixer.music.play()
    for x in range(100):
        volume = x/100
        mixer.music.set_volume(volume)  
        sleep(0.1)
        print(volume)
        
def fade_out_music():
    #there is an inbuilt pygame fadeout but I didn't like it
    print("Music fading out")
    
    for x in range(100):
        volume = x/100
        mixer.music.set_volume(1-volume)  
        sleep(0.1)
        print(volume)
    mixer.music.stop()


fade_in_music()
#fade_out_musicy()
fade_out_music()
# idea: maybe link the light level to volume?

