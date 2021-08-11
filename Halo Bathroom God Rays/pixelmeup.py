import board
import neopixel

#https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage
pixels = neopixel.NeoPixel(board.D18, 18)
from time import sleep


# thanks to Adam Luchjenbroers for this mapping https://stackoverflow.com/a/1969274
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return int(rightMin + (valueScaled * rightSpan))

humidityCurrent = 82
humidityMax = 100
humidityMin = 0


ledPosition = translate(humidityCurrent,humidityMin,humidityMax,1,18)
print(ledPosition)

for x in range(ledPosition):
    pixels[x] = (40, 40, 20)
    sleep(0.05)
    
for x in range(ledPosition):
    pixels[x] = (40, 40, 0)
    sleep(0.05)
    
sleep(0.5)

ledPosition = translate(humidityCurrent,humidityMin,humidityMax,1,18)
print(ledPosition)
    
for x in range(ledPosition):
    pixels[x] = (20, 20, 40)
    sleep(0.05)
    
for x in range(ledPosition):
    pixels[x] = (0, 0, 40)
    sleep(0.05)
    
    
"""
pixels[0] = (40, 0, 0)

sleep(2)
pixels.fill((0, 60, 0))
"""