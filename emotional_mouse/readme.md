## Emotional Mouse Project

This is a computer mouse that makes an cute/angry noise if you're too rought with it. It gets stressed out. Starts shaking the cursor.
Then you have to pick it up and calm it down. 

Parts needed:

A computer mouse to butcher
A small sound sensor
A Raspi Pico
A speakersound board

Project notes for me:

The mouse coloured cables are

Brown - G   GND
Blue -  V   +5V
White - C   Data
Green - D   Data


Rough instructions:

Disconnect the mouse's internal Infrared LED from the mouse and hook it up to GPIO17 and GND instead so that the pico can control if the mouse actually works or not depending on the mood of the mouse. Make not of positive and neg before disconnecting.

Pull back the insulation on the +5V and GND wires to the mouse. Solder 2 wires off of them to steal their power. You can use that to power your pico and the speaker. 



Should investigate PWM sound output to ditch the bulky relay. Or find a smaller relay. 
