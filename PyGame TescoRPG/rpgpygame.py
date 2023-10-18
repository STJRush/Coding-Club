
import random, statistics
import matplotlib.pyplot as plt
from time import sleep
from colorama import Fore, Style
from fractions import Fraction
from decimal import Decimal

def d(n): #rolls a dice eg d(8) or d(20)
  roll = random.randint(1,n)+1
  return roll

#quick toggles
sneakAttackToggle=True #assuming sneak attacks
adv=False #assuming advantage
debug=False #set to True for narration

###############################################
# Change These Stats for Different Characters #
###############################################
characterLevel=3
profBonus=3
dexModifier=3
strengthModifier=1
###############################################

atkbonus = dexModifier + profBonus #weapon or spell attack bonus

#parameters
simCount=9000
missCount=0
simSpeed = 2.8

#variables to declare before using
bonusActionDmg = 0
dmglist=[]


print(" ")
print("      _,.    ")
print("     ,` -.)  ")
print("    ( _/-\\-._      ")
print("   /,|`--._,-^|            ,   ")
print("   \_| |`-._/||          ,'|  ")
print("     |  `-, / |         /  /  ")
print("     |     || |        /  /           D&D Attack Damage Simulator ")
print("      `r-._||/   __   /  /               Rogue 3 / Fighter 2 ")
print("  __,-<_     )`-/  `./  /  ")
print(" '  \   `---'   \   /  /  ")
print("     |           |./  /            Should I attack this monster or run? ")
print("     /           //  /  ")
print(" \_/' \         |/  /  ")
print(" |    |   _,^-'/  /               This program will simulate 9001 attacks ")
print("  |    , ``  (\/  /_              and let you know what damage you can do")
print("   \,.->._    \X-=/^  ")
print("   (  /   `-._//^`  ")
print("    `Y-.____(__}  ")
print("     |     {__)  ")
print("           ()  ")
print("   ")
print("This program also has a debug mode to narrate a single action.")
print("It also takes into account Critical Hits ie. Rolling a 20 \n \n")

print("0-13 No Armour    15-17 Medium Amour   18+ Heavy Armour \n")

aC=int(input("Please enter the Armour Class of your opponent eg. 22  "))

print("If your oppenant is on the ground or flanked, you have advantage.")


if debug==True:
    simCount=1


for x in range(simCount): #how many attacks to simulate

  # weapons for characters

  #dex weapons (default)
  shortsword = d(6)+dexModifier
  rapier = d(8)+dexModifier
  heavyCrossbow = 1*d(10)+dexModifier
  longbow = 1*d(8)+dexModifier
  shortbow = 1*d(6)+dexModifier
  scimitar= 1*d(6)+dexModifier

  #strength weapons (change attack bonus)
  longsword = 1*d(8)+strengthModifier
  spear = 1*d(6)+strengthModifier

  #special modifiers
  sneakAttack = 2*d(6)
  
  ###############################################
  # Change These Stats for Different Characters #
  ###############################################

  #Weapons equiped for each attack
  #The A,B and C parts of the weapon attacks allow for smites, extra damage rolls, sneak attacks etc.

  weapon1A=rapier
  weapon1B=sneakAttack
  weapon1C=0

  weapon2A=shortsword
  weapon2B=0
  weapon2C=0

  weaponBonusActionA=0
  weaponBonusActionB=0
  weaponBonusActionC=0

  ###############################################
  
  #1st attack damage comes from
  atk1Dmg = weapon1A + weapon1B + weapon1C

  #2nd attack damage comes from
  atk2Dmg = weapon2A + weapon2B +weapon2C

  bonusActionDmg = weaponBonusActionA + weaponBonusActionB + weaponBonusActionC
  #Bonus attack damage comes from
  #Not setup for this character yet
    
  atk1DiceRoll=d(20)
  if debug==True:
    print("You swing your blade down from the heavens above!")
    print("Rolling a d20 dice to attack..")
    sleep(simSpeed)
    print("You roll a ", atk1DiceRoll)
    sleep(simSpeed)


  atkRoll1=atk1DiceRoll+atkbonus   #add your attack bonus to your roll

  if debug==True:
    print("A level Rogue 3 / Fighter 2  has an attack bonus of +",atkbonus,", so in total that's a ", atkRoll1, "to hit." )
    sleep(simSpeed)

  if adv==True: #check for advantage
      advantagedAttackroll=d(20)+atkbonus #roll again
      if advantagedAttackroll >=atkRoll1:
        atkRoll1=advantagedAttackroll  #take higher roll

        if debug==True:
          print("Oh wait!.. With advantage you roll again and take the higher roll of", atkRoll1)
          sleep(simSpeed)


        

  if atkRoll1>=aC:  #check if it hits

    if debug==True:
          print("So an attack of ", atkRoll1, " to hit an AC of", aC)
          sleep(simSpeed)
          print("That's a hit!")
          print("Your strike lands home! Your opponent does not look happy!")
          sleep(simSpeed)
    

    if debug==True:
          print("Your first attack does damage of ", atk1Dmg)
          sleep(simSpeed)

    if atk1DiceRoll==20:
    
      if debug==True:
            print("FIRST ATTACK IS A CRITICAL HIT!!!")
            sleep(simSpeed)
            print("Damage of ", atk1Dmg, " is doubled!!!!")
            sleep(simSpeed)

      atk1Dmg=atk1Dmg*2  #CRITICAL HIT, DOUBLE IT UP!

      if debug==True:
            print("First attack does a damage of ",atk1Dmg)


  else:
    atk1Dmg=0 # you miss so no damage for you
  
    if debug==True:
            print("FIRST ATTACK IS A MISS!")
            print("Your strike rattles off the opponent's armour!")
            sleep(simSpeed)




#THE SECOND ATTACK

  atk2=d(20)

  if debug==True:
    print("")
    print("Here comes the offhand attack...")
    sleep(1)
    print("Your roll a ", atk2)
    sleep(simSpeed)

  atk2=atk2+atkbonus   #add your attack bonus to your roll
  
  if debug==True:
    
    print("So a with an attack bonus of +", atkbonus, "is.." )
    sleep(simSpeed)
    print(atk2, "to hit...")
    sleep(simSpeed)

  if adv==True: #check for advantage
    atkadv=d(20)+atkbonus #roll again
    if atkadv >=atk2:
      atk2=atkadv  #take higher roll

      if debug==True:
          print("with advantage, takes the higher roll of", atkadv-atkbonus)
          sleep(simSpeed)

  if atk2>=aC:  #check if it hits

    if debug==True:
          print("So an attack of ", atk2, " to hit an AC of", aC)
          sleep(simSpeed)
          print("That's a hit!")
          sleep(simSpeed)

    if (atk2-atkbonus)==20: #Natural 20

      if debug==True:
            print("SECOND ATTACK IS A CRITICAL HIT!!!")
            print("Damage of ", atk2Dmg, " is doubled")
            sleep(simSpeed)

      atk2Dmg=atk2Dmg*2  #CRITICAL HIT
    
    if debug==True:
            print("offhand attack damge is ", atk2Dmg)
            sleep(simSpeed)
            
  else:

    atk2Dmg=0 

    if debug==True:
            print("OFFHAND ATTACK IS A MISS!")
            print("Your opponent steps under your swing and takes no damage.")
            sleep(simSpeed)



#BONUS ACTION DAMAGE:
  bonusActionDmg = 0


#ADD IT ALL UP
  dmg= atk1Dmg + atk2Dmg + bonusActionDmg #the plus one here is a bug fix for red lines showing up
                                 # in matplot graphs. It's silly.

  dmglist.append(dmg)
  
if debug==True:
  print("Total damage fo this action is..")
  print(dmglist)


if debug==False:

  

  print(dmglist)
  print("")

  print("For an Armour class of ", aC)


  #calculate how many misses by counting them
  for item in dmglist:
    if item ==0:  #1 is a miss
      missCount+=1
  
  print(Style.BRIGHT+"")
  print(Fore.RED + "-Odds of missing are ", round((missCount/simCount)*100,2),"%")
  print(Fore.GREEN + "-Odds of hitting are ",100-round((missCount/simCount)*100,2),"%")
  
  


  

  #mode and mean
  likelyDamage=statistics.mean(dmglist)
  freqDamage=statistics.mode(dmglist)
  medianDamage=statistics.median(dmglist)

  #round() just rounds the number

  
  print(Fore.CYAN+" \nWHETHER YOU HIT OR NOT:")
  print(" - Mean damage: ", round(likelyDamage))
  print(" - Median damage: ", round(medianDamage))
  print(" - Most often:", freqDamage , " (this is the mode).")
  
  #the mode is pretty useless when there's no bell curve eg. one attack instead of two

  

  hitsWithoutMisses=[]

  for item in dmglist:
    if item !=0:
      hitsWithoutMisses.append(item)
  
  

  #mode and mean if you do hit
  likelyDamage=statistics.median(hitsWithoutMisses)
  freqDamage=statistics.mode(hitsWithoutMisses)
  medianDamage=statistics.median(hitsWithoutMisses)

  print(Fore.YELLOW+" \nIF YOU DO HIT...")
  print(" - Mean damage:", round(likelyDamage,2))
  print(" - Median damage:", round(medianDamage,2))
  print(" - Most often ",freqDamage, " (this is the mode).")
  print(Style.RESET_ALL)

  sortedThings=list(set(dmglist))
  
  print("BEST AND WORST:")
  print("\n The bottom ten worst possible damage outcomes:")
  print(sortedThings[:10])

  print("\n The top ten best possible damage outcomes:")
  print(sortedThings[-10:])

  print(Fore.YELLOW+" ")
  actualDamage=int(input("\n What damage did you get? "))
 
  print("\n So a dice was rolled 9001 times, generating ", len(sortedThings), "unique possible outcomes")
  
  for item in sortedThings:
    if item == actualDamage:
      nth=sortedThings.index(item)+1

  print("\n You got a damage of ", actualDamage)
  print("\n Of the",len(sortedThings), " possible outcomes, that's like number", nth," from the bottom.")

  print("\n However not all of the", len(sortedThings), "outcomes are equally likely, far from it!")



  yourOutcomeCounter = 0    
  for item in dmglist:
    if item == actualDamage:
      yourOutcomeCounter+=1


  decimalOddsy=round(yourOutcomeCounter/simCount,4)
  decimalOddsy2=round(yourOutcomeCounter/simCount,2)

  percentageOddsy=yourOutcomeCounter/simCount*100
  
  #to cover extremes I had to do two round downs
  oddsy=Fraction(Decimal(decimalOddsy)).limit_denominator(10000)
  oddsy2=Fraction(Decimal(decimalOddsy)).limit_denominator(100)

  print(Fore.RED + " ")
  print("\n Your actual chances of getting ", actualDamage, " are about", oddsy, "or roughly", oddsy2)

  print("Or as a percent", round(percentageOddsy,2),"%")

  print(Style.RESET_ALL)

 

  plt.hist(dmglist, density=1, bins=10) #plots a histogram
  #uses values from the list called dmglist. Histogram split into 10 segments.

  plt.axis([0, 120, 0, 0.1]) #limts of x and y axis
  #axis([xmin,xmax,ymin,ymax])
  plt.xlabel('Damage')
  plt.ylabel('Chance')

  plt.plot(dmglist) #plots the thing

  plt.savefig('plots.png') #saves it as a png for printing
  plt.show()#shows it on the console window too
  sleep(2)
  plt.close()
  plt.exit()
  
  
