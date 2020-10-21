
def tesco():
    
    while True:
       
        choice = input("where do you want to go? (s)upervalu")
        
        if choice == "s":
            print("You head on down for some super valu")
            supervalu()
        
        else:
            print("you stay in Tesco. ...... You're still in Tesco. ....sigh..")


def supervalu():
    print("In your bag:", listy)
    
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
    
    print("Two seaguls step out into your path and thow you a filty look like a flying howyaz")
    print("One goes for your phone")
    
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
        
                  
        print("Bird health:", birdhealth)
        print("Your health:", playerHealth)
        
        action = input("Do you (s)mack it or (r)un?")
        
        if action == "s":
            print(namey, " commits an act of animal cruelty")
            birdhealth = birdhealth - 5
               
        elif action == "r":
            print("You can't escape a seagul! It hits you!")
            playerHealth = playerHealth - 1
            
        if playerHealth == 0:
            raise ImaJustGonaCrashPythonYoureThatBad
            
    
    print("\n The bird is gone. Val comes out and gives you a some breaded chicken")
    
    listy.append("breaded chicken")
    print("In your bag:", listy)
    
    
    
listy = []     

#NAME                    
print("You see a Tesco Security guard approach you")

namey = input("What is your Name!??!!??!")

print(namey, "?, What are you from Lusk?")


#WHERE TO GO?
tesco()

    
print("game over")
