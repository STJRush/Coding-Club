#starts pygame
from time import sleep
import pygame
pygame.init()

#sets the window size
gameDisplay = pygame.display.set_mode((800,600))

#loads in your pics to use later
pokeScreen1 = pygame.image.load('village.PNG')
garyImg = pygame.image.load('ash.png')

#SET BACKGROUND COLOUR
gameDisplay.fill((0,0,0)) # paints black



def tesco():
    
    while True:
        
        choice = input("where do you want to go? (s)upervalu")
        
        if choice == "s":
            print("You head on down for some super valu")
            supervalu()
        
        else:
            print("you stay in Tesco. ...... You're still in Tesco. ....sigh..")


def supervalu():
    
    
    while True:
        
        print("It's still supervalu.")
        
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
    print("You're standing at the T junction by the butchers. It's the village takeaway!")
    
    
#DISPLAY PICS

gameDisplay.blit(pokeScreen1, (80,80))
 #puts pokemon background at 

for i in range (0, 500, 5):
    gameDisplay.blit(garyImg, (i,90)) #puts car at 70,90 on top of last picture.
    pygame.display.update()
    sleep(0.01)
    

#if you add a pic, you need to update the screen to show it
pygame.display.update()





#Escape from Tesco Car Park

#NAME                    
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
