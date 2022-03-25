# Found at https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
# Credit to Adrian Rosebrock

from PCA9685 import PCA9685
from time import ctime

# import the necessary packages
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM) 
GPIO.setup(14, GPIO.OUT)

#opencv stuff
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2

#servo hat stuff
pwm = PCA9685(0x40)
pwm.setPWMFreq(50)

#initialize some variables
lasercounter = 0 
xCenter = 250
yCenter = 250

def center():
    pwm.setServoPulse(0,1300)
    pwm.setServoPulse(1,1300) 
    time.sleep(1)

#center servos at program start
center()

# construct the argument parser and parse the arguments
# changing "default" below alters sensitivity. 500 was default but 10,000 is good far large objects only.
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=9000, help="minimum area size")
args = vars(ap.parse_args())



# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	vs = VideoStream(src=0).start()
	time.sleep(2.0)
	
# otherwise, we are reading from a video file
else:
	vs = cv2.VideoCapture(args["video"])
	
# initialize the first frame in the video stream
firstFrame = None

# loop over the frames of the qvideo
while True:
	# grab the current frame and initialize the occupied/unoccupied
	# text
	frame = vs.read()
	frame = frame if args.get("video", None) is None else frame[1]
	text = "Unoccupied"
	# if the frame could not be grabbed, then we have reached the end
	# of the video
	
	if frame is None:
		break
	# resize the frame, convert it to grayscale, and blur it
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)
	# if the first frame is None, initialize it
	if firstFrame is None:
		firstFrame = gray
		continue
	
		# compute the absolute difference between the current frame and
	# first frame
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	# loop over the contours
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < args["min_area"]:
			continue
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		
		#get the center of the rectangle and draw a circle in it
		xCenter= x + w//2
		yCenter= y + h//2
		cv2.circle(frame,(xCenter,yCenter), 10, (0,0,255), 2)
		
		text = "Occupied. X=" + str(xCenter) + " Y=" + str(yCenter)
		# draw the text and timestamp on the frame
	cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
	# show the frame and record if the user presses a key
	cv2.imshow("Security Feed", frame)
	cv2.imshow("Thresh", thresh)
	cv2.imshow("Frame Delta", frameDelta)
	key = cv2.waitKey(1) & 0xFF
	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break
	
	lasercounter = lasercounter + 1
	#print(lasercounter)
	if lasercounter == 50: # smaller more flashy, bigger less flashy, default is 30
	
		GPIO.output(14, GPIO.HIGH)
		time.sleep(0.1)
		GPIO.output(14, GPIO.LOW)
		lasercounter = 0
		
		print("xCenter is ", xCenter)
		print("servoSettingx is ", servoSettingx)
		print("yCenter is ", yCenter)
		print("servoSettingy is ", servoSettingy)
		
	# default is -0.7*xCenter+1600
	servoSettingx=-0.8*xCenter+1600
	pwm.setServoPulse(0,servoSettingx)
	
	# default is -0.6*xCenter+1200
	servoSettingy=10*yCenter+1200
	pwm.setServoPulse(1,servoSettingy)
		
		
		
        
		
# cleanup the camera and close any open windows
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()

#center and power down servos to stop that weird sizzling servo noise
center()
pwm.setPWM(0, 0, 4096)
pwm.setPWM(1, 0, 4096)
GPIO.cleanup()

print("Safe shutdown. Well done on pressing 'q' instead of stop.")