from picamera import PiCamera
from time import sleep


camera = PiCamera()


camera.start_preview()
camera.start_recording('/home/pi/Desktop/video.h264')
sleep(20)
camera.stop_recording()
camera.capture('/home/pi/Desktop/image.jpg')
sleep(5)
camera.stop_preview()

