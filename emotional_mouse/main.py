# emotional mouse code
from machine import Pin
import time

led = Pin("LED", machine.Pin.OUT)
led.off()
time.sleep(1)
c=0
pinIn = Pin(15, Pin.IN,Pin.PULL_UP) # sensor pin
pinOut = Pin(16, Pin.OUT) # output pin

print("Starting..")


while True:
    
    if pinIn.value(): # if we see an input signal on Pin15
        led.on()
        print("We get signal")
        pinOut.value(1) # turns on output Pin16
        time.sleep(1)
    else:
        led.off()
        pinOut.value(0) # turns off output Pin16
        
        # report nothing yet every 10 cycles to confirm program still running
        c=c+1
        if c%10 == 1:
            print("nothing yet")
            
    time.sleep(0.1)
    
print("done")


for x in range(4):
    led.on()
    time.sleep(0.1)
    led.off()
    time.sleep(0.1)
