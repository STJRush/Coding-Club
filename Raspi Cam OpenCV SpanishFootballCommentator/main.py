from pygame import mixer 
from time import sleep
mixer.init()


def fade_in_music():
    
    print("Music fading in")
    
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
        print(1-volume)
        
    mixer.music.stop()

# Part 1/3: HOW TO PLAY MUSIC  --------------------------------
 
# 1. Load the song. (Music files should be .mp3 files)



mixer.music.load("cheeringmusic.mp3") # This .mp3 needs to be in the same folder as your .py python file
  
# 2. Set the volume
mixer.music.set_volume(0.6) 
  
# 3. Start playing the song, allowing time (sleep in seconds) for it to play
mixer.music.play()


print("Playing music now!")




sleep(1)


# Part 2/3: HOW TO PLAY SOUNDS: --------------------------------


# 1. Load in sounds ready to play later (SOUND CLIPS must be .wav or .ogg files and can NOT be .mp3)

gol1= mixer.Sound("GOL1.wav") # make up a variable name eg.engageSound
gol2= mixer.Sound("GOL2.wav") # these sound clips must be in the same folder as your python file
gol3= mixer.Sound("GOL3.wav") # these sound clips must be in the same folder as your python file
gol4= mixer.Sound("GOL4.wav") # these sound clips must be in the same folder as your python file
buildup1= mixer.Sound("buildUpLavae.wav") # these sound clips must be in the same folder as your python file
buildup2= mixer.Sound("Buildup2Quick.wav") # these sound clips must be in the same folder as your python file
miss1= mixer.Sound("miss1.wav")
miss2= mixer.Sound("miss2.wav")
penalty= mixer.Sound("Penalty.wav")

sleep(2)

mixer.Sound.play(buildup1) 
sleep(2)
mixer.Sound.stop(buildup1)

mixer.Sound.play(gol4) 
sleep(6)
mixer.Sound.stop(gol4)

sleep(4)
mixer.Sound.play(penalty)
sleep(14)
mixer.music.stop()

#ideas:

# Pre-draw squares on screen using openCV to align the goals and baounderies
# Hold up a red card to trigger PENALTY, maybe this will be the first to test



