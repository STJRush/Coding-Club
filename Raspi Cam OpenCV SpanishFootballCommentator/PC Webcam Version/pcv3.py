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

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Mouse callback function to capture clicks
def click_and_crop(event, x, y, flags, param):
    global refPt, cropping, setup_mode, goal_count

    if setup_mode and event == cv2.EVENT_LBUTTONDOWN:
        refPt.append((x, y))
        cropping = True

# Define the yellow color range in HSV
yellow_lower = np.array([20, 100, 100], dtype="uint8")
yellow_upper = np.array([30, 255, 255], dtype="uint8")

# Variables for setting up goals
setup_mode = False
cropping = False
refPt = []
goals = []

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", click_and_crop)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    if setup_mode:
        cv2.putText(frame, "Click on goal corners to trace (8 total points, 4 per goal)", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

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

                # Check if the point is inside any of the goal areas
                for index, goal in enumerate(goals):
                    if cv2.pointPolygonTest(np.array(goal, dtype=np.int32), (x, y), False) >= 0:
                        if mixer.get_busy() != 1:
                            random_Sound = random.choice(golSounds)
                            random_Sound.play()
                            print(f"Goal in area {index+1}!")

    if len(refPt) == 8:
        goals = [refPt[:4], refPt[4:]]
        setup_mode = False
        print("Goals set up complete.")

    for goal in goals:
        if len(goal) == 4:
            cv2.polylines(frame, [np.array(goal, dtype=np.int32)], isClosed=True, color=(0, 255, 0), thickness=2)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    if key == ord('g'):
        setup_mode = True
        refPt = []
        print("Setup mode entered. Click to define goals.")

    if key == ord('\r'):  # Enter key to finalize the setup
        if setup_mode and len(refPt) == 8:
            setup_mode = False
            print("Setup mode exited. Goals are set.")

# Cleanup
cap.release()
cv2.destroyAllWindows()
mixer.quit()
