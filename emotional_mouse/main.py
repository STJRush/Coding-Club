# An emotional mouse code
from machine import Pin
import time

# sets up internal LED on pico
interalLED = Pin("LED", machine.Pin.OUT)

# Setup of GPIO Pins
pinIn15 = Pin(15, Pin.IN,Pin.PULL_UP) # sensor pin
soundPin16 = Pin(16, Pin.OUT) # output pin for relay control of Sound Board
mouseLEDPin17 = Pin(17, Pin.OUT) # output pin led that controls mouse


# test button
button = Pin(6, Pin.IN, Pin.PULL_UP)

# initialize counter for later
i=0

print("Starting..")

interalLED.on()
time.sleep(0.5)
interalLED.off()

# Turn on mouse motion tracking LED (The one that's normally on the mouse)
mouseLEDPin17.on()

while True:
    
    # if we see an input signal on Pin15...
    if pinIn15.value(): 
        # interalLED.on() # turn on the interal LED (debugging)
        print("We get signal")
        soundPin16.on() # turns on output Pin16 to trigger relay-> soundboard
        
        # turn off/on the mouse for a bit to punish user for being too rough
        mouseLEDPin17.off()
        time.sleep(0.5)
        mouseLEDPin17.on()
        time.sleep(1)
        mouseLEDPin17.off()
        time.sleep(1)
        mouseLEDPin17.on()
        
    elif button.value() == 0:
        print("Button Test Pushed")
        soundPin16.on()
        time.sleep(0.5)
        
        
    else:
        # interalLED.off()  (debugging)
        soundPin16.off() # turns off output Pin16 to stop playing sound
        
        # print "nothing yet" every 10 cycles to confirm program still running
        i=i+1
        if i%10 == 1:
            print("nothing yet")
            
            # flash LED to show it's working if no PC connected
            interalLED.on()
            time.sleep(0.2)
            interalLED.off()
    
    #tick interval
    time.sleep(0.1)
    
    
"""
Raspberry Pi Pico
https://www.raspberrypi.com/documentation/microcontrollers/images/pico-pinout.svg

WiFi Chip Facing You
   _______
 __[     ]__
[  [MICRO]  ]
[  [ USB ]  ]
[  [_____]  ]
[           ]
[ 0    VBUS ]            Fantastic GPIO Pins and where to find them
[ 1    VSYS ] 
[ GND  GND  ]       <----   GND is 3rd pin down from top right near USB
[ 2    3V3  ] (EN) 
[ 3    3v3  ] (OUT) <----   +3V is 5th pin down from top right near USB
[ 4    REF  ] (ADC_VREF)
[ 5    28   ] (ADC2) <----  Analogue Input is 7th pin down from top right near USB
[ GND  GND  ] (AGND)
[ 6    27   ] (ADC1)
[ 7    26   ] (ADC0)
[ 8    RUN  ]
[ 9    22   ]
[ GND  GND  ]
[ 10   21   ]
[ 11   20   ]
[ 12   19   ]
[ 13   18   ]
[ GND  GND  ] <----   GND is 3rd pin up on the right from the bottom of the Pico, either side.
[ 14   17   ] <----   GPIO17 is 2nd last pin down from top right near USB (IN THIS PROJECT: MOUSE MOTION RED LED)
[ 15   16   ] <----   GPIO16 is last pin down from top right near USB (IN THIS PROJECT: RELAY/SOUNDBOARD)
[   o o o   ]
 -----------
 
 
 FROM UNDERNEATH:
 
    _____ 
 __[_____]__
[           ]
[           ]
[           ]
[           ]
[ VBUS  0   ]          
[ VSYS  1   ] 
[ GND  GND  ]       <----   GND is 3rd pin down from top right near USB
[ 3V3   2   ]
[ 3v3   3   ] 
[ RED   4   ] 
[ 28    5   ] (ADC2) is GP28
[ GND  GND  ] (AGND)
[ 27    6   ] (ADC1) is GP27
[ 26    7   ] (ADC0) is GP26
[ RUN   8   ]
[ 22    9   ]
[ GND  GND  ]
[ 21   10   ]
[ 20   11   ]
[ 19   12   ]
[ 18   13   ]
[ GND  GND  ] <----   GND is 3rd pin up on the right from the bottom of the Pico, either side.
[ 17   14   ] <----   GPIO17 (IN THIS PROJECT: MOUSE MOTION RED LED)
[ 16   15   ] <----   GPIO16 (IN THIS PROJECT: RELAY/SOUNDBOARD)
[   o o o   ]
 -----------
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
"""

