# These 3 lines of code must go at the top of your program for sounds or music to work
# You need to also install the pygame module from "Tools>Manage Packages>" & search pygame

from pygame import mixer 
from time import sleep
mixer.init() 
  
  
# Part 1/3: HOW TO PLAY MUSIC  --------------------------------
 
# 1. Load the song. (Music files should be .mp3 files)
mixer.music.load("nextgenTheme.mp3") # This .mp3 needs to be in the same folder as your .py python file
  
# 2. Set the volume
mixer.music.set_volume(0.7) 
  
# 3. Start playing the song, allowing time (sleep in seconds) for it to play
mixer.music.play()


print("Playing music now!")
sleep(1)
print("this")
sleep(3)
print("and STOPPING")


mixer.music.stop()

sleep(1)


# Part 2/3: HOW TO PLAY SOUNDS: --------------------------------


# 1. Load in sounds ready to play later (SOUND CLIPS must be .wav or .ogg files and can NOT be .mp3)

engageSound= mixer.Sound("picard.wav") # make up a variable name eg.engageSound
makitsoSound= mixer.Sound("makitso.wav") # these sound clips must be in the same folder as your python file

print("Now playing two .wav sound clips")
sleep(1)

#plays clip
mixer.Sound.play(engageSound) 
sleep(2)

#plays clip
mixer.Sound.play(makitsoSound)
sleep(1)


# Part 3/3: HOW TO PLAY SOUND OVER SOME MUSIC --------------------------------
print("Now playing a .wav sound effect over some music")

#starts music
mixer.music.play()
sleep(2)
#plays sound clip (loaded above)
mixer.Sound.play(makitsoSound)
sleep(1)
#stops music
mixer.music.stop()

#note: Those last few lines won't work without first loading the sound in parts 1/3 and 2/3





