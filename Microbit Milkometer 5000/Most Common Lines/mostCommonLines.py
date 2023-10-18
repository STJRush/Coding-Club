#find and list repeated lines from a book (txt file)
import re

print("                                                                    ")
print("              .__=\__                  .__==__,         Most        ")
print("            jf       ~~=\,         _=/~       `\,       Common      ")
print("        ._jZ             `\q,   /=~             `\__    Lines       ")
print("       j5(/                 `\./                  V\\,              ")
print("     .Z))' _____              |             .____, \)/\   -D.Murray ")
print("    j5(K=~~     ~~~~\=_,      |      _/=~~~~     `~~+K\\,           ")
print("  .Z)\/                `~=L   |  _=/~                 t\ZL          ")
print(" j5(_/.__/===========\__   ~q |j/   .__============___/\J(N,        ")
print(" 4L#XXXL_________________XGm, \P  .mXL_________________JXXXW8L      ")
print("")

print("Opening the book..")
bookFile = open("alice.txt","r") # Open the file
string=bookFile.read()  #reads the whole book into a big big giant string for python.
string=string.lower() #make it all lowercase. GeTs riD of THis. i!=I , l!=L, p !=P etc.
bookFile.close() #python has the string in it's head now, so can close the text file.

#clean up the file and put each sentence on a new line

clean_string= re.sub("\n", " ", string)    #join it all back up into one long long line.

clean_string= re.sub("\.\.\.\.\.\.", "", clean_string)
clean_string= re.sub("\.\.\.\.\.", "", clean_string)
clean_string= re.sub("\.\.\.\.\.", "", clean_string)     #get rid of ....
clean_string= re.sub("\.\.\.\.", "", clean_string)
clean_string= re.sub("\.\.\.", "", clean_string)
clean_string= re.sub("\.\.", "", clean_string)

clean_string= re.sub("\. \. \. \.", "", clean_string)
clean_string= re.sub("\. \. \.", "", clean_string)      #get rid of . . . . . 
clean_string= re.sub("\. \.", "", clean_string)

clean_string= re.sub("\.", "\n", clean_string)
clean_string= re.sub("\?", "\n", clean_string)    #make these all markers for new lines
clean_string= re.sub("\!", "\n", clean_string)

clean_string= re.sub("         ", "", clean_string)
clean_string= re.sub("        ", "", clean_string)
clean_string= re.sub("       ", "", clean_string)
clean_string= re.sub("      ", "", clean_string)   #get rid of random spaces in the document
clean_string= re.sub("     ", "", clean_string)
clean_string= re.sub("    ", "", clean_string)
clean_string= re.sub("   ", "", clean_string)
clean_string= re.sub("  ", "", clean_string)


# The next part writes the cleaned up file to a text file that I can open to check it
# all looks nice and neat and ready for finding duplicate lines.

newFile = open("editedVersion.txt", "w") #creates new text file called editedVersion
newFile.write(clean_string) #writes the big long edited string to a this txt file
newFile.close() #closes the file

#Right, lets open this file again and find some duplicate lines.
#Wait why did you close if if you were going to use it again straight away?
#Yeah I just wanted to be sure it's worked up to this point and I can't look at the text file
#without having python close it properly. It's nice to be able to open and view the edited
#text file that you're about to work with to check it's clean.

newFile = open("editedVersion.txt", "r") #opens the file again. 
allBookLinesInAList=newFile.readlines() #reads it all into a big big string in it's head

#figures out how many lines there so the program knows when to stop.
totalNumberOfLines=len(allBookLinesInAList)
print("This book has", totalNumberOfLines, "lines")
print("This would take about", totalNumberOfLines//23, "minutes to read")
if totalNumberOfLines>3000:
    print("This is actually pretty big. This could take up to ", totalNumberOfLines//400, "seconds..")
print("Okay, here we go")
print("========================================================")

finalList=[]  #prepares an empty list to print the matching lines into later

#The bit below makes takes a line (n) and compares it to all lines after it (z)
#It might help to imaging "n" as your left finger keeping track of the row and "z" as your right finger going across the columns

n=0
while n<totalNumberOfLines:  #no point in comparing past the number of lines in the doc!
    z=1
    while z<totalNumberOfLines:            
            try:
                if allBookLinesInAList[n]==allBookLinesInAList[n+z]:
                    finalList.append(allBookLinesInAList[n])
                z=z+1
                
                #print(n,z)
                    
            except (IndexError):
                break
    n=n+1

newFile.close()

for i in set(finalList):  #goes throught the final list and prints each item
    print(i)              #the set() removes duplicates eg. said harry, said harry

print("=================================================")
print("The lines above were all repeated at least once.\n")
print("Have a nice day!")
