#!/usr/bin/env python3
#v3.1

import os
from sense_hat import SenseHat
import RPi.GPIO as GPIO
import pygame
import time
from threading import Timer

# skip intro flag
play_intro = True

# Initialize Sense HAT
sense = SenseHat()

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
relay_pin = 21
GPIO.setup(relay_pin, GPIO.OUT)
GPIO.output(relay_pin, GPIO.LOW)

# Initialize Pygame mixer
pygame.mixer.init()

# Read MP3 files from the /songs directory
songs_folder = '/home/pi/PartyWizard/songs'




mp3_files = [
    os.path.join(songs_folder, file)
    for file in sorted(os.listdir(songs_folder))
    if file.endswith('.mp3')
]

current_index = 0
music_playing = False
disco_on = False
disco_timer = None  # Timer object for managing delayed disco light activation

# Define a rainbow pattern (8x8)
rainbow_pixels = [
    (255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0), (0, 255, 0),  (0, 255, 128), (0, 255, 255), (0, 128, 255),
    (255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0), (0, 255, 0),  (0, 255, 128), (0, 255, 255), (0, 128, 255),
    (255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0), (0, 255, 0),  (0, 255, 128), (0, 255, 255), (0, 128, 255),
    (255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0), (0, 255, 0),  (0, 255, 128), (0, 255, 255), (0, 128, 255),
    (255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0), (0, 255, 0),  (0, 255, 128), (0, 255, 255), (0, 128, 255),
    (255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0), (0, 255, 0),  (0, 255, 128), (0, 255, 255), (0, 128, 255),
    (255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0), (0, 255, 0),  (0, 255, 128), (0, 255, 255), (0, 128, 255),
    (255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0), (0, 255, 0),  (0, 255, 128), (0, 255, 255), (0, 128, 255)
]

# Define a rsmielyface
smileyFace = [
    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 255), (0, 0, 255),  (0, 0, 0), (0, 0, 0), (0, 0, 0),
    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),  (0, 0, 0), (0, 0, 0), (0, 0, 0),
    (0, 0, 0), (0, 255, 255), (0, 0, 0), (0, 0, 0), (0, 0, 0),  (0, 0, 0), (0, 255, 255), (0, 0, 0),
    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),  (0, 0, 0), (0, 0, 0), (0, 0, 0),
    (255, 0, 255), (255, 0, 255), (255, 0, 255), (255, 0, 255), (255, 0, 255),  (255, 0, 255), (255, 0, 255), (255, 0, 255),
    (0, 0, 0), (0, 0, 0), (255,  0, 255), (0, 0, 0), (0, 0, 0),  (0, 0, 0), (255, 0, 255), (0, 0, 0),
    (0, 0, 0), (0, 0, 0), (255, 0, 255), (0, 0, 0), (0, 0, 0),  (255, 0, 255), (0, 0, 0), (0, 0, 0),
    (0, 0, 0), (0, 0, 0), (0, 0, 0), (255, 0, 255), (255, 0, 255),  (0, 0, 0), (0, 0, 0), (0, 0, 0)
]

def set_rainbow():
    sense.set_pixels(rainbow_pixels)
    
def set_smiley():
    sense.set_pixels(smileyFace)

def show_message(message, scroll_speed=0.02):
    # Display the message upside-down
    sense.set_rotation(180)
    sense.show_message(message, scroll_speed=scroll_speed)
    sense.set_rotation(0)

def fill_screen_with_colors():
    # Fill the screen with Red, Green, and Blue sequentially for 5 seconds
    
    for x in range(12):
        for color in [(255, 0, 0), (0, 255, 0), (0, 0, 255)]:
            sense.clear(color)
            time.sleep(0.43)  # ~5 seconds total divided among the colors
    sense.clear()

def start_disco_timer(song_name): #KICK IN THE LIGHTS ON CUE AT COOL PARTS IN SONG
    global disco_timer
    if song_name.startswith("4"): # I will survive
        disco_timer = Timer(23.5, lambda: GPIO.output(relay_pin, GPIO.HIGH))
    elif song_name.startswith("5"): # gimmie gimmie
        disco_timer = Timer(18, lambda: GPIO.output(relay_pin, GPIO.HIGH))
    elif song_name.startswith("2"): # venga boys we like to party
        disco_timer = Timer(31, lambda: GPIO.output(relay_pin, GPIO.HIGH))
    elif song_name.startswith("6"): # tetris techno
        disco_timer = Timer(35, lambda: GPIO.output(relay_pin, GPIO.HIGH))
    elif song_name.startswith("7"): # seven nation army
        disco_timer = Timer(9.5, lambda: GPIO.output(relay_pin, GPIO.HIGH))
    else:
        disco_timer = None

    if disco_timer:
        disco_timer.start()

def stop_disco_timer():
    global disco_timer
    if disco_timer:
        disco_timer.cancel()
        disco_timer = None
    GPIO.output(relay_pin, GPIO.LOW)  # Ensure the relay is turned off

# Play the intro song and display the initial message
intro_song = '/home/pi/PartyWizard/songs/IntroSongs/PWizardIntro.mp3'


if play_intro == True:
    if os.path.exists(intro_song):
        pygame.mixer.music.load(intro_song)
        pygame.mixer.music.play()
    
        show_message("Party Wizard")
        fill_screen_with_colors()
        pygame.mixer.music.stop()
    else:
        print("No intro?")
    set_smiley()

while True:
    for event in sense.stick.get_events():
        if event.action == 'pressed':
            
            if event.direction == 'right':
                print("right")
                current_index = (current_index - 1) % len(mp3_files)
                show_message(os.path.basename(mp3_files[current_index]))
                sense.set_rotation(180)
                print(current_index)
                sense.show_letter(str(current_index+1), text_colour=[255, 0, 100])
                #time.sleep(1)
                #sense.set_rotation(0)
                

            elif event.direction == 'left':
                print("left")
                current_index = (current_index + 1) % len(mp3_files)
                show_message(os.path.basename(mp3_files[current_index]))
                sense.set_rotation(180)
                sense.show_letter(str(current_index+1), text_colour=[255, 0, 0])
                #time.sleep(1)
                #sense.set_rotation(0)
                

            elif event.direction == 'up':
                if not music_playing:
                    # Play the selected song
                    selected_song = mp3_files[current_index]
                    pygame.mixer.music.load(selected_song)
                    pygame.mixer.music.play()
                    set_rainbow()
                    start_disco_timer(os.path.basename(selected_song))
                    music_playing = True
                else:
                    # Stop music and reset disco
                    pygame.mixer.music.stop()
                    stop_disco_timer()
                    sense.clear()
                    music_playing = False

            elif event.direction == 'down':
                # Manual toggle of the disco lights
                disco_on = not disco_on
                GPIO.output(relay_pin, GPIO.HIGH if disco_on else GPIO.LOW)

    time.sleep(0.05)

