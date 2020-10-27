#starts pygame
from time import sleep
import pygame
pygame.init()

#sets up pygame music
from pygame import mixer
mixer.init()

#Loads the music file
mixer.music.load("IntroSong.mp3") # This .mp3 needs to be in the same folder as your .py python file
mixer.music.play()

global gameDisplay

#sets the window size
gameDisplay = pygame.display.set_mode((800,600))

#loads in your pics to use later
pokeScreen1 = pygame.image.load('tescofront.png')
tescoPic = pygame.image.load('outTes.png')
superPic = pygame.image.load('superOut.png')
garyImg = pygame.image.load('ash.png')

#SET BACKGROUND COLOUR
gameDisplay.fill((0,0,0)) # paints black



def tesco():
    #Display Tesco Outside
    gameDisplay = pygame.display.set_mode((800,600))
    gameDisplay.fill((0,0,0)) # paints black
    gameDisplay.blit(tescoPic, (0,0))
    
    #Display Text over Image
    myfont = pygame.font.Font("game_over.ttf", 100)
    label = myfont.render("Welcome to Tesco "+namey, 1, (0,0,255))
    # put the label object on the screen at point x=100, y=100
    gameDisplay.blit(label, (200, 500))

    #Show changes
    pygame.display.update()
    

    mixer.music.stop()
    
    while True:
              
        #Loads the music file
        mixer.music.load("TescoSong.mp3") # This .mp3 needs to be in the same folder as your .py python file
        mixer.music.play()
        

        print("\n \n Ah the smell of car exhaust, bins, baked goods and flowers and wet dog.")
        print("A sinking feeling of corporate emptiness that unites the six nations more than rugby")
        print("It's a big feck off Tesco building with a bottle bank in the carpark")
        sleep(0.3)
        
        choice = input("where do you want to go? (s)upervalu")
        
        if choice == "s":
            print("You head on down for some super valu")
            mixer.music.stop()
            supervalu()
        
        else:
            print("you stay in Tesco. ...... You're still in Tesco. ....sigh..")


def supervalu():
    print("\n \n SuperValu...")
    print(" SuperValu never changes")
    sleep(0.3)
    print("\n \n Every town in Ireland has a supervalu with one primary function:")
    print("That function is to provide teenagers with stories about working in Supervalu")
    print("The 'kinda sound' junior managers, the scary managers, the mysterious owner...")
    sleep(0.3)
    print("You just wanted money to buy stuff and your Dad wanted you to see THE REAL WORLD")
    print("You will later discover Supervalu is thankfully only a small part of the world")
    sleep(0.3)
    print("\n There will be renovations. ")
    sleep(0.3)
    print("\n There will be 'new managment'")
    sleep(0.3)
    print("\n But SuperValu? Supervalu never changes...")
    print("")
    
    #Display SuperValu Outside
    gameDisplay = pygame.display.set_mode((800,600))
    gameDisplay.fill((0,0,0)) # paints black
    gameDisplay.blit(superPic, (0,0))
    
    #Display Text over Image
    myfont = pygame.font.Font("game_over.ttf", 100)
    label = myfont.render("Welcome to Supervalu", 1, (255,0,0))
    # put the label object on the screen at point x=100, y=100
    gameDisplay.blit(label, (200, 50))

    #Show changes
    pygame.display.update()

    
    mixer.music.stop()
    
    while True:
        
        mixer.music.load("StockClerk.mp3") # This .mp3 needs to be in the same folder as your .py python file
        mixer.music.play()
        
        print("It's still Supervalu.")
        
        choice = input("Sigh...where do you want to go now? (t)esco?, (v)illage?")

        if choice == "t":
            print("You head on down to tesco yet again")
            tesco()
            
        elif choice == "v":
            print("You head on down to val in the village")
            village()

        else:
            print("you stay in Supervalu. ...... You're still in Supervalu. ....sigh..")

def village():
    
    mixer.music.stop()
    mixer.music.load("gullBattle.mp3") # This .mp3 needs to be in the same folder as your .py python file
    mixer.music.play()
    
    print("\n \n You're standing at the T junction by the butchers. It's the village takeaway!")
    sleep(2)
    print("Two seaguls step out into your path and thow you a filty look like a flying howyaz")
    print("One goes for your phone")
    sleep(2)
    birdhealth  = 10
    playerHealth = 10
    
   
    
    while birdhealth>0:
        
        print(" \n\n    ")
        print("      ███████████")
        print("  ███████ █ █ ████  ")
        print("     █████████████                       ")
        print("      ██  \       ██                        ")
        print("████████ ██       ██                        ")
        print("██░░░░██          ██                        ")
        print("████████          ██                        ")
        print("      ████      ████                        ")
        print("        ██      ██                          ")
        print("      ████      ████                         ")
        print("        ███    ███                          ")
        print("        ██ █  ███                           ")
        print("        ██  ██  ██                          ")
        print("      ████      ████████████████████████████ ")
        print("      ██             ██░░░░░░░░░░░░░░░░░░░░██ ")
        print("      ██  [    ]     ██░░░░░░addidas░░ ░ ░ ░██ ")
        print("      ██   [  ]      ██░░░░░░░░░░░░░░░░░░░░██ ")
        print("      ██             ████████████████████████ ")
        print("      ██                                  ██ ")
        print("      ██████████████████████████████████████ ")
        print("        ██░░██  ██░░██                   ")   
        print("        ██░░██  ██░░██           ")           
        print("        ██░░██  ██░░██       ")               
        print("    ██████░░██████░░██         ")             
        print("    ██ ░ ░ ░██ ░ ░ ░██       ")               
        print("    ██████████████████   \n\n  ")
        
                  
        print("Flyin Howyaz health:", birdhealth)
        print("Your health:", playerHealth)
        
        action = input("Do you (s)mack it or (r)un for your life?")
        
        if action == "s":
            print(namey, " commits an act of animal cruelty")
            sleep(1.2)
            birdhealth = birdhealth - 2
               
        elif action == "r":
            print("You can't escape a seagul! IT CAN FLY! It hits you!")
            sleep(1.2)
            playerHealth = playerHealth - 1
            
        if playerHealth == 0:
            raise ImaJustGonaCrashPythonYoureThatBad
            
    
    print("\n The bird is gone. Val comes out and gives you a some breaded chicken")
    
    listy.append("breaded chicken")
    print("In your bag:", listy)
    


listy = []

#DISPLAY BACKGROUND AND CHARACTER

sleep(1)

for i in range (0, 500, 15):
    gameDisplay.blit(pokeScreen1, (0,0))
    gameDisplay.blit(garyImg, (i,250)) #puts car at 70,90 on top of last picture.
    pygame.display.update()
    sleep(0.01)

sleep(1.3)



# Chooses a font with size 270 (you can download fonts as
# .ttf files from font websites and put them
# in the python folder like sounds or music)

myfont = pygame.font.Font("game_over.ttf", 270)
# apply it to text on a label

#Display Main Label of TESCO RPG
label = myfont.render("TESCO RPG", 1, (255,0,0))
# put the label object on the screen at point x=100, y=100
gameDisplay.blit(label, (100, 100))
pygame.display.update()


sleep(2)


#Display smaller "Press Start" text

#reload the font to be a smaller size (just 100)
myfont = pygame.font.Font("game_over.ttf", 100)
label = myfont.render("Press Enter", 1, (0,0,0))
# put the label object on the screen at point x=100, y=100
gameDisplay.blit(label, (250, 300))
#if you add a pic, you need to update the screen to show it
pygame.display.update()





#MAIN GAME STARTS HERE

z = input("Press enter to start")

#ENTER A NAME
sleep(0.3)
print("You see a Tesco Security guard approach you")
namey = input("What is your Name!??!!??!")
print(namey, "?, What are you from Lusk?")


#WHERE TO GO?
tesco()

    
print("game over")



#This line just stops the game from closing at the end
input("Finished game, press the anykey")

pygame.quit()
quit()
