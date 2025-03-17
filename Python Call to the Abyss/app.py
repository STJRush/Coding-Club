import csv
import random

# Load the outcome table from CSV into a dictionary
def load_outcome_table(filename):
    outcome_table = {}
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            key = int(row["Roll"])
            outcome_table[key] = {
                "Result": row["Outcome"],
                "Description": row["Description"]
            }
    return outcome_table

# Load door labels from CSV into a dictionary keyed by level
def load_door_labels(filename):
    door_labels = {}
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            level = int(row["Level"])
            door_labels[level] = {
                "Language": row["Language"],
                "Up": row["Up"],
                "Down": row["Down"]
            }
    return door_labels

def map_d4_to_outcome(d4_roll):
    mapping = {1: 6, 2: 9, 3: 12, 4: 14}
    return mapping.get(d4_roll, 10)

def call_to_abyss(current_level, outcome_table):
    print(f"\n[Call to the Abyss] - Current Abyss Level: {current_level}")
    if current_level <= 4:
        print("You are in the shallow layers. Please roll a d4 (enter a number between 1 and 4):")
        roll = int(input("Your d4 roll: "))
        while roll < 1 or roll > 4:
            print("Invalid roll. Please enter a number between 1 and 4:")
            roll = int(input("Your d4 roll: "))
        outcome_roll = map_d4_to_outcome(roll)
        print(f"(Your d4 roll of {roll} maps to an outcome roll of {outcome_roll}.)")
    else:
        print("Please roll a d20 (enter a number between 1 and 20):")
        outcome_roll = int(input("Your d20 roll: "))
        while outcome_roll < 1 or outcome_roll > 20:
            print("Invalid roll. Please enter a number between 1 and 20:")
            outcome_roll = int(input("Your d20 roll: "))
    
    outcome = outcome_table.get(outcome_roll, {"Result": "Unknown", "Description": "No description available."})
    wish = input("State your wish: ")
    narrative = f"Your wish was: '{wish}'\nOutcome ({outcome_roll} - {outcome['Result']}): {outcome['Description']}"
    print("\n" + "="*40)
    print(narrative)
    print("="*40 + "\n")

def summon_door(current_level, door_labels):
    print("\n[Summon a Door]")
    # Ensure current level doesn't exceed available door labels (use level 99 if so)
    label_level = current_level if current_level <= 99 else 99
    labels = door_labels.get(label_level, {"Language": "Unknown", "Up": "Up", "Down": "Down"})
    
    # Randomly assign door roles: one door is "up" and the other is "down"
    if random.random() < 0.5:
        door1_role = "up"
        door2_role = "down"
    else:
        door1_role = "down"
        door2_role = "up"
    
    # Prepare the door labels using the lost language words.
    door1_label = labels["Up"] if door1_role == "up" else labels["Down"]
    door2_label = labels["Up"] if door2_role == "up" else labels["Down"]
    
    # Display the doors to the players.
    print(f"In the language of {labels['Language']}, you see two doors:")
    print(f"   Door 1: '{door1_label}'")
    print(f"   Door 2: '{door2_label}'")
    print("(In English: the door labeled with the 'up' word means 'Ascend' and the one with the 'down' word means 'Descend'.)")
    
    choice = input("Which door do you choose? Type '1' or '2': ").strip()
    while choice not in ["1", "2"]:
        print("Invalid choice. Please type '1' or '2'.")
        choice = input("Which door do you choose? Type '1' or '2': ").strip()
    
    if choice == "1":
        chosen = door1_role
    else:
        chosen = door2_role

    if chosen == "up":
        if current_level == 1:
            new_level = 0  # Exit the abyss.
            print(f"You choose Door {choice}. It leads upward—you ascend and escape the abyss! ⬆️")
        else:
            new_level = current_level - 1
            print(f"You choose Door {choice}. It leads upward—you ascend one level! ⬆️")
    else:  # chosen == "down"
        new_level = current_level + 1
        print(f"You choose Door {choice}. It leads downward—you descend one level! ⬇️")
    
    print(f"You are now on abyss level: {new_level}\n")
    return new_level

def main():
    outcome_table = load_outcome_table("outcome_table.csv")
    door_labels = load_door_labels("door_labels.csv")
    current_level = 1
    print("Welcome to the Abyssal Gateway!\n")
    
    while True:
        print(f"Current Abyss Level: {current_level}")
        if current_level <= 4:
            print("In these shallow layers, your wishes are limited. (Use a d4, which maps to outcomes between 6 and 14.)")
        else:
            print("In these deeper layers, roll a d20 for your wish outcomes.")
        
        print("Options:")
        print("1. Call to the Abyss")
        print("2. Summon a Door")
        print("3. Quit")
        choice = input("Enter your choice (1/2/3): ")
        
        if choice == "1":
            call_to_abyss(current_level, outcome_table)
        elif choice == "2":
            current_level = summon_door(current_level, door_labels)
            if current_level == 0:
                print("You have successfully escaped the abyss. Congratulations!")
                break
        elif choice == "3":
            print("Thanks for playing!")
            break
        else:
            print("Invalid option. Please choose 1, 2, or 3.")
            
if __name__ == "__main__":
    main()
