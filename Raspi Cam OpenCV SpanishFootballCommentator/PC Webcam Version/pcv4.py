import cv2
import numpy as np
from pygame import mixer
import random

# Initialize the pygame mixer for audio
mixer.init()
mixer.music.load("cheeringmusic.mp3")
mixer.music.set_volume(0.6)
mixer.music.play()

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

# Define the yellow color range in HSV
yellow_lower = np.array([20, 100, 100], dtype="uint8")
yellow_upper = np.array([30, 255, 255], dtype="uint8")

# Variables for setting up goals
setup_mode = False
refPt = []
goals = []
scale_origin = None

def click_and_crop(event, x, y, flags, param):
    global refPt, setup_mode

    if setup_mode and event == cv2.EVENT_LBUTTONDOWN:
        refPt.append((x, y))

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", click_and_crop)

def draw_scale(frame, origin, length=400):
    """Draw a linear scale from origin point horizontally."""
    cv2.line(frame, origin, (origin[0] + length, origin[1]), (255, 0, 0), 2)
    for i in range(11):  # Draw marks for every 10%
        x = origin[0] + int(i * length / 10)
        cv2.line(frame, (x, origin[1] - 10), (x, origin[1] + 10), (255, 0, 0), 2)
        cv2.putText(frame, str(i * 10), (x - 10, origin[1] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)

while True:
    ret, frame = cap.read()
    if not ret:
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

    if setup_mode:
        cv2.putText(frame, "Click on goal corners to trace (8 total points, 4 per goal)", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    if len(refPt) == 8:
        goals = [refPt[:4], refPt[4:]]
        mid_point = ((refPt[3][0] + refPt[7][0]) // 2, (refPt[3][1] + refPt[7][1]) // 2)
        scale_origin = (mid_point[0] - 200, mid_point[1])
        setup_mode = False
        draw_scale(frame, scale_origin)
    
    for goal in goals:
        if len(goal) == 4:
            cv2.polylines(frame, [np.array(goal, dtype=np.int32)], isClosed=True, color=(0, 255, 0), thickness=2)

   
