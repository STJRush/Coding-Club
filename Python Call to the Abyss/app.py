
print("Welcome to the Abyss")
import numpy as np
import cv2
import csv
import random
import threading
import time
import pygame
import numpy as np
from openai import OpenAI
from mysecrets import API_KEY  # Import your API key from mysecrets.py

# Initialize the OpenAI client using the API key from mysecrets.py.
client = OpenAI(api_key=API_KEY)

# Global variables for controlling the audio and video threads.
risk_volume = 0.1  # default volume is 10%
stop_audio = False
stop_video = False
current_vortex_speed = 0.3  # initial video speed

# Global channels for audio fade out.
music_channel = None
crackle_channel = None

# Reinitialize pygame mixer with custom parameters (adjustable for testing)
pygame.mixer.quit()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
print("Pygame mixer initialized with frequency=44100, size=-16, channels=2, buffer=512.")

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

def map_risk_roll(roll, dice_max):
    """
    Map the player's roll from the chosen dice to a value between 1 and 20.
    For d4 we use a custom mapping; for others we linearly interpolate.
    """
    if dice_max == 4:
        mapping = {1: 6, 2: 9, 3: 12, 4: 14}
        return mapping[roll]
    else:
        new_roll = 1 + (roll - 1) * (19 / (dice_max - 1))
        return round(new_roll)

def get_vortex_speed_from_dice(dice_max):
    """
    Returns the playback speed factor for the vortex video.
    For 1d4, speed is 0.3x; for 1d20, speed is 2.0x; linear interpolation for intermediate dice.
    """
    if dice_max == 4:
        return 0.3
    else:
        return 0.3 + (2.0 - 0.3) * ((dice_max - 4) / (20 - 4))

def get_crackle_volume(dice_max):
    """
    Returns the volume for the crackle.ogg sound.
    For 1d4, volume is 0.2 (20%), and for 1d20, volume is 1.0 (100%).
    Linear interpolation for intermediate dice.
    """
    if dice_max == 4:
        return 0.2
    else:
        return 0.2 + (dice_max - 4) * ((1.0 - 0.2) / (20 - 4))

def play_vortex_video():
    """
    Plays the video 'vortex.mp4' in a loop.
    The playback speed is controlled via the global 'current_vortex_speed'.
    The loop exits when the global 'stop_video' flag is set.
    """
    cap = cv2.VideoCapture("vortex.mp4")
    if not cap.isOpened():
        print("Error: Could not open vortex.mp4")
        return
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 30  # fallback
    while not stop_video:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        delay = int(1000 / fps / current_vortex_speed)
        cv2.imshow("Vortex", frame)
        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break
    cap.release()
    # Do not call cv2.destroyAllWindows() here.

def play_abyss_audio():
    """
    Plays two audio streams concurrently using separate channels:
      - 'music.mp3' on channel 0 at full volume.
      - 'crackle.ogg' on channel 1 with volume set by the global 'risk_volume'.
    Updates the crackle volume periodically until stop_audio is True.
    """
    global risk_volume, stop_audio, music_channel, crackle_channel
    music_sound = pygame.mixer.Sound("music.mp3")
    crackle_sound = pygame.mixer.Sound("crackle.ogg")
    
    music_channel = pygame.mixer.Channel(0)
    crackle_channel = pygame.mixer.Channel(1)
    
    music_channel.play(music_sound, loops=-1)
    music_channel.set_volume(1.0)
    
    crackle_channel.play(crackle_sound, loops=-1)
    crackle_channel.set_volume(risk_volume)
    
    #print("Audio channels started: music on channel 0, crackle on channel 1.")
    
    while not stop_audio:
        crackle_channel.set_volume(risk_volume)
        time.sleep(0.5)
    
    music_channel.stop()
    crackle_channel.stop()

def fade_out():
    """
    Gradually reduces the vortex video playback speed back to 0.3x.
    Then prompts the user: "Press ENTER to close the vortex and fade out music."
    Once ENTER is pressed, the program will fade out the music volume and then close the OpenCV window.
    Plays a crash sound ("crash.ogg") at the start.
    """
    global current_vortex_speed, music_channel, stop_video
    #print("Playing crash sound...")
    crash_sound = pygame.mixer.Sound("crash.ogg")
    crash_sound.play()
    #print("Crash sound played.")
    
    # Fade out video speed from current value back to 0.3x.
    fade_duration = 5.0  # seconds
    fade_steps = 20
    step_delay = fade_duration / fade_steps
    target_speed = 0.3
    initial_speed = current_vortex_speed
    speed_diff = initial_speed - target_speed
    #print(f"Fading video speed from {initial_speed} to {target_speed} over {fade_steps} steps.")
    for i in range(fade_steps):
        current_vortex_speed = initial_speed - speed_diff * ((i+1) / fade_steps)
        # Uncomment for debugging:
        # print(f"Fade step {i+1}/{fade_steps}: current_vortex_speed = {current_vortex_speed:.2f}")
        time.sleep(step_delay)
    #print("Video speed fade-out complete.")
    
    # Now prompt the user to close the vortex.
    input("Press ENTER to close the vortex and fade out music...")
    
    # Signal the video thread to stop.
    print("Setting stop_video flag to True.")
    stop_video = True
    time.sleep(0.5)  # Allow time for the video thread to finish its loop.
    
    # Close OpenCV windows.
    print("Closing OpenCV windows...")
    cv2.destroyAllWindows()
    print("OpenCV windows closed.")
    
    # Fade out music volume gradually.
    print("Fading out music...")
    fade_duration = 5.0  # seconds
    fade_steps = 20
    step_delay = fade_duration / fade_steps
    initial_music_volume = music_channel.get_volume() if music_channel else 1.0
    for i in range(fade_steps):
        new_vol = initial_music_volume * (1 - ((i+1) / fade_steps))
        if music_channel:
            music_channel.set_volume(new_vol)
        # Uncomment for debugging:
        # print(f"Music fade step {i+1}/{fade_steps}: volume set to {new_vol:.2f}")
        time.sleep(step_delay)
    print("Music fade-out complete.")

def call_to_abyss(current_level, outcome_table):
    global current_vortex_speed, stop_audio, risk_volume, stop_video
    print(f"\n[Call to the Abyss] - Current Abyss Level: {current_level}")
    
    # Start vortex video in a separate thread.
    current_vortex_speed = 0.3  # initial speed
    stop_video = False
    video_thread = threading.Thread(target=play_vortex_video)
    video_thread.start()
    
    # Start audio playback in a separate thread.
    risk_volume = 0.1  # default initial volume is 10%
    stop_audio = False
    audio_thread = threading.Thread(target=play_abyss_audio)
    audio_thread.start()
    
    # Prompt the player to state their wish first.
    wish = input("State your wish: ")
    
    # Let the player choose their risk die.
    print("Choose your risk die:")
    print("1. 1d4")
    print("2. 1d8")
    print("3. 1d10")
    print("4. 1d12")
    print("5. 1d20")
    dice_choice = input("Enter your choice (1-5): ").strip()
    while dice_choice not in ["1", "2", "3", "4", "5"]:
        print("Invalid choice. Please enter a number between 1 and 5.")
        dice_choice = input("Enter your choice (1-5): ").strip()
        
    dice_options = {
         "1": {"type": "d4", "max": 4},
         "2": {"type": "d8", "max": 8},
         "3": {"type": "d10", "max": 10},
         "4": {"type": "d12", "max": 12},
         "5": {"type": "d20", "max": 20}
    }
    chosen_dice = dice_options[dice_choice]
    dice_max = chosen_dice["max"]
    
    # Update vortex speed and crackle volume based on chosen risk die.
    current_vortex_speed = get_vortex_speed_from_dice(dice_max)
    risk_volume = get_crackle_volume(dice_max)
    print(f"Vortex video speed updated to {current_vortex_speed:.1f}x and crackle volume set to {risk_volume*100:.0f}% based on your chosen risk die ({chosen_dice['type']}).")
    
    # Play the 'strike.ogg' sound to signal risk level selection.
    strike_sound = pygame.mixer.Sound("strike.ogg")
    strike_sound.play()
    
    # Prompt the player to roll their chosen die.
    print(f"Please roll your {chosen_dice['type']} (enter a number between 1 and {dice_max}):")
    roll = int(input(f"Your {chosen_dice['type']} roll: "))
    while roll < 1 or roll > dice_max:
         print(f"Invalid roll. Please enter a number between 1 and {dice_max}:")
         roll = int(input(f"Your {chosen_dice['type']} roll: "))
    
    outcome_roll = map_risk_roll(roll, dice_max)
    print(f"(Your {chosen_dice['type']} roll of {roll} maps to an outcome roll of {outcome_roll}.)")
    
    outcome = outcome_table.get(outcome_roll, {"Result": "Unknown", "Description": "No description available."})
    
    # Use the ChatGPT completions API to generate the narrative.
    system_message = (
        f"You are the magical abyss. A player has rolled a {outcome_roll} on the dice. "
        f"The outcome is '{outcome['Result']}'. {outcome['Description']} "
        "Describe in the second person tense, in bullet points, 4 ways in which the player's wish is affected by this outcome. Ensure that these outcomes are not game breaking and maximize narrative potential and player engagement."
    )
    user_message = wish
    print("Generating narrative response from ChatGPT...")
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
    )
    narrative = completion.choices[0].message.content
    print("\n" + "="*40)
    print(narrative)
    print("="*40 + "\n")
    
    # Fade out the video speed and audio only after the user presses ENTER.
    fade_out()
    
    # Stop the audio and video threads.
    stop_audio = True
    audio_thread.join()
    stop_video = True
    video_thread.join()

def summon_door(current_level, door_labels):
    print("\n[Summon a Door]")
    label_level = current_level if current_level <= 99 else 99
    labels = door_labels.get(label_level, {"Language": "Unknown", "Up": "Up", "Down": "Down"})
    
    if random.random() < 0.5:
        door1_role = "up"
        door2_role = "down"
    else:
        door1_role = "down"
        door2_role = "up"
    
    door1_label = labels["Up"] if door1_role == "up" else labels["Down"]
    door2_label = labels["Up"] if door2_role == "up" else labels["Down"]
    
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
    else:
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
            print("In these shallow layers, your wishes are limited.")
        else:
            print("In these deeper layers, roll a d20 for your wish outcomes.")
        
        print("Options:")
        print("1. Call to the Abyss")
        print("2. Summon a Door")
        print("3. Quit")
        choice = input("Enter your choice (1/2/3): ")
        
        if choice == "1":
            global stop_audio, stop_video
            stop_audio = False
            stop_video = False
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
