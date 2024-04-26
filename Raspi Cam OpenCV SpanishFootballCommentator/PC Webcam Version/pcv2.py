import cv2
import numpy as np
from pygame import mixer 
import random

# Initialize the pygame mixer for audio
mixer.init()

# Load sound files
mixer.music.load("cheeringmusic.mp3")
mixer.music.set_volume(0.6)
mixer.music.play()
print("Playing cheering background noise now!")

# Sound effects
gol1 = mixer.Sound("GOL1.wav")
gol2 = mixer.Sound("GOL2.wav")
gol3 = mixer.Sound("GOL3.wav")
gol4 = mixer.Sound("GOL4.wav")
buildup1 = mixer.Sound("buildUpLavae.wav")
buildup2 = mixer.Sound("Buildup2Quick.wav")
miss1 = mixer.Sound("miss1.wav")
miss2 = mixer.Sound("miss2.wav")
penalty = mixer.Sound("Penalty.wav")

golSounds = [gol1, gol2, gol3, gol4]
buildupSounds = [buildup1, buildup2]

# Define the yellow color range in HSV
yellow_lower = np.array([20, 100, 100], dtype="uint8")
yellow_upper = np.array([30, 255, 255], dtype="uint8")

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Goal boundaries initial position
goal1x, goal1y, goal1w, goal1h = 100, 100, 50, 200
goal2x, goal2y, goal2w, goal2h = 500, 100, 50, 200

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                x = int(M["m10"] / M["m00"])
                y = int(M["m01"] / M["m00"])
                cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
                print(x, y)

                # Check for goals or near goals
                if x > goal1x and x < goal1x + goal1w and y > goal1y and y < goal1y + goal1h:
                    if mixer.get_busy() != 1:
                        random_Sound = random.choice(golSounds)
                        random_Sound.play()
                    print("LEFT GOAL")

                if x > goal2x and x < goal2x + goal2w and y > goal2y and y < goal2y + goal2h:
                    if mixer.get_busy() != 1:
                        random_Sound = random.choice(golSounds)
                        random_Sound.play()
                    print("RIGHT GOAL")

    # Draw the goal boundaries on the frame
    cv2.rectangle(frame, (goal1x, goal1y), (goal1x + goal1w, goal1y + goal1h), (0, 0, 255), 2)
    cv2.rectangle(frame, (goal2x, goal2y), (goal2x + goal2w, goal2y + goal2h), (255, 0, 0), 2)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
mixer.quit()
