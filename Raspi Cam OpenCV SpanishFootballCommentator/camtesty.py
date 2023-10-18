from picamera import PiCamera
from time import sleep

camera = PiCamera()

# show what the camera sees for 3 seconds 
camera.start_preview()
sleep(3)
camera.stop_preview()