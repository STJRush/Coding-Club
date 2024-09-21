
# Initalize player scores 
player1_points = 0
player2_points = 0

# Choose your move
player1_choice = "coop"
player2_choice = "coop"


# Award Points

# both cooperate
if player1_choice == "coop" and player2_choice == "coop":
    player1_points += 3
    player2_points += 3

# player 1 outright win
if player1_choice == "coop" and player2_choice == "def":
    player1_points += 5

# player 2 outright win
if player1_choice == "def" and player2_choice == "coop":
    player2_points += 5

# both defect
if player1_choice == "def" and player2_choice == "def":
    player1_points += 1
    player2_points += 1


print("P1 Points:", player1_points)
print("P2 Points:", player2_points)