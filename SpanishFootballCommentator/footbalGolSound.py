'''
Object detection ("Ball tracking") with OpenCV
    Adapted from the original code developed by Adrian Rosebrock
    Visit original post: https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
Developed by Marcelo Rovai - MJRoBot.org @ 7Feb2018 
'''

from pygame import mixer 
from time import sleep
mixer.init()

import random

import keyboard

# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2

# 1. Load the song. (Music files should be .mp3 files)
mixer.music.load("cheeringmusic.mp3") # This .mp3 needs to be in the same folder as your .py python file
  
# 2. Set the volume
mixer.music.set_volume(0.6) 
  
# 3. Start playing the song, allowing time (sleep in seconds) for it to play
mixer.music.play()


print("Playing cheering background noise now!")

# 1. Load in sounds ready to play later (SOUND CLIPS must be .wav or .ogg files and can NOT be .mp3)

gol1= mixer.Sound("GOL1.wav") # make up a variable name eg.engageSound
gol2= mixer.Sound("GOL2.wav") # these sound clips must be in the same folder as your python file
gol3= mixer.Sound("GOL3.wav") # these sound clips must be in the same folder as your python file
gol4= mixer.Sound("GOL4.wav") # these sound clips must be in the same folder as your python file
buildup1= mixer.Sound("buildUpLavae.wav") # these sound clips must be in the same folder as your python file
buildup2= mixer.Sound("Buildup2Quick.wav") # these sound clips must be in the same folder as your python file
miss1= mixer.Sound("miss1.wav")
miss2= mixer.Sound("miss2.wav")
penalty= mixer.Sound("Penalty.wav")

golSounds = [gol1,gol2,gol3,gol4]
buildupSounds = [buildup1, buildup2]

speedCounter = 0


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "yellow object"
# (or "ball") in the HSV color space, then initialize the
# list of tracked points
colorLower = (20, 50, 50)
colorUpper = (60, 255, 255)
pts = deque(maxlen=args["buffer"])
 
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	camera = cv2.VideoCapture(0)
 
# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])
x=1
y=1
# left goal starting variables
goal1x=0
goal1y=200
goal1h=100
goal1w=100

# right goal starting variables
goal2x=500
goal2y=200
goal2h=100
goal2w=100

# keep looping
while True:
	# grab the current frame
	(grabbed, frame) = camera.read()
 
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if args.get("video") and not grabbed:
		break
 
	# resize the frame, inverted ("vertical flip" w/ 180degrees),
	# blur it, and convert it to the HSV color space
	frame = imutils.resize(frame, width=600)
	frame = imutils.rotate(frame, angle=360)
	# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, colorLower, colorUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	
	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	
	# Left Goal Red
	cv2.rectangle(frame, (goal1x, goal1y), (goal1x + goal1w, goal1y + goal1h), (0, 0, 255), 2)
	
	text = "Red Goal"
	cv2.putText(frame, "Red goal".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	
	# Right Goal Blue
	cv2.rectangle(frame, (goal2x, goal2y), (goal2x + goal2w, goal2y + goal2h), (255, 0, 0), 2)
	
	#move square (requires root)
	if keyboard.is_pressed('d'):
	 goal1x=goal1x+20
	 sleep(0.2)
	elif keyboard.is_pressed('a'):
	 goal1x=goal1x-20
	 sleep(0.2) 
	elif keyboard.is_pressed('w'):
	 goal1y=goal1y-20
	 sleep(0.2) 
	elif keyboard.is_pressed('s'):
	 goal1y=goal1y+20
	 sleep(0.2)
	elif keyboard.is_pressed('z'):
	 goal1h=goal1h+20
	 sleep(0.2)
	elif keyboard.is_pressed('c'):
	 goal1h=goal1h-20
	 sleep(0.2)
	elif keyboard.is_pressed('q'):
	 goal1w=goal1w+20
	 sleep(0.2)
	elif keyboard.is_pressed('e'):
	 goal1w=goal1w-20
	 sleep(0.2)
	 
	text = "Blue Goal"
	cv2.putText(frame, "Blue goal".format(text), (510, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
	

	
	"""
	#get the center of the rectangle and draw a circle in it
	xCenter= x + w//2
	yCenter= y + h//2
	cv2.circle(frame,(xCenter,yCenter), 10, (0,0,255), 2)
	"""
	
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
 
		# only proceed if the radius meets a minimum size
		if radius > 2: # default 10
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			print(x,y)
 
	# update the points queue
	pts.appendleft(center)
	
		# loop over the set of tracked points
	for i in range(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue
 
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
 
	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# if the 'r' key is pressed, stop the loop
	if key == ord("r"):
		break
	
	#GOL 1 (LEFT) Checker
	if (x > goal1x) and (x < goal1x+goal1w) and (y > goal1y and y <(goal1y+goal1h)):
	         #mixer.pause()
	         if mixer.get_busy() != 1:
	            random_Sound = random.choice(golSounds)
	            random_Sound.play()
	         print("LEFT GOAL")
	
	            
	#GOL 2 (RIGHT) Checker
	if (x > goal2x) and (x < goal2x+goal2w) and (y > goal2y and y <(goal2y+goal2h)):
	         if mixer.get_busy() != 1:
	            random_Sound = random.choice(golSounds)
	            random_Sound.play()
	         print("RIGHT GOAL")
	            
	#NearGOL Chekcer
	if (x > goal1x+goal1w and x <goal1x+goal1w+50) or (x > 400 and x <500):
	         if mixer.get_busy() != 1:
	            random_Buildup_Sound = random.choice(buildupSounds)
	            random_Buildup_Sound.play()
	         print("Near goal")
	
	            
	
	            

 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
