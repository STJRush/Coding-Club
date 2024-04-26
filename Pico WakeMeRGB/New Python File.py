import network
import time
import utime
import ntptime
import urequests

from machine import Pin

# internal led
led = machine.Pin("LED", machine.Pin.OUT)
led.on()


def connect_to_wifi(ssid, password):
    
    flashInteralLED()
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    if wlan.isconnected():
        print("Online")
        led.on()
    else:
        print("Error connecting to WiFi")

def get_time():
    response = urequests.get("http://worldtimeapi.org/api/timezone/Europe/London")
    json_data = response.json()
    datetime_str = json_data['datetime']  # format: "2023-11-01T12:34:56.789123+00:00"
    hour = int(datetime_str[11:13])
    return hour


"""

    RGB LED Wiring Diagram
       _______
      |    ¬  |
      |       |
      |_______|
     /  |   |  \
    /   |   |   \
    |   |   |   |
    |   |   |   |
    |   |   |   |
    |   |   |   |
    R   |   G   B
        GND
  
Pins on the pico
   GP2  G  GP1 GP0  
    |   |   |   |
"""
# THIS BIT I CHANGED FOR THE PIXEL
rled = Pin(2, Pin.OUT)
gled = Pin(1, Pin.OUT)
bled = Pin(0, Pin.OUT)

def flashInteralLED():
    for x in range(3):
        led.on()
        utime.sleep(0.2)
        led.off()
        utime.sleep(0.2)

def lightsOut():
    rled.off()
    gled.off()
    bled.off()

def red():
    rled.on()

def green():
    gled.on()

def blue():
    bled.on()

def purple(): # looked just red?
    rled.on()
    bled.on()


def blueGreen():
    gled.on()
    bled.on()

def greenOrange():
    gled.on()
    rled.on()
    
def redTripleFlashy():
    for x in range(3):
        rled.on()
        utime.sleep(0.2)
        rled.off()
        utime.sleep(0.2)
        
def redFlashyForever():
    rled.on()
    utime.sleep(0.2)
    rled.off()
    utime.sleep(0.2)  
    
def blueTripleFlashy():
    for x in range(3):
        bled.on()
        utime.sleep(0.2)
        bled.off()
        utime.sleep(0.2)


def blueFlashyForever():
    bled.on()
    utime.sleep(0.3)
    bled.off()
    utime.sleep(0.3)


def bootup_colour_rainbow():


    red()
    utime.sleep(0.8)
    lightsOut()

    purple()
    utime.sleep(0.8)
    lightsOut()

    green()
    utime.sleep(0.8)
    lightsOut()

    blueGreen()
    utime.sleep(0.8)
    lightsOut()

    blue()
    utime.sleep(0.8)
    lightsOut()

    redTripleFlashy()
    blueTripleFlashy()
    


# start

ssid = ""
password = ""

connect_to_wifi(ssid, password)
bootup_colour_rainbow()
led.off()

while True:

    if network.WLAN(network.STA_IF).isconnected():
        #flashInteralLED()
        hour = get_time()
        
        print("Current time: {}:00".format(hour))
        
        if hour >= 19 or hour < 7:
            print("Red for Bed")
            red()
        elif hour >= 7 < 8:
            print("Green for getting up")
            green()
        else:
            print("Day time blue")
            blue()
        
        utime.sleep(30)  # wait for 60 seconds before checking again
        
    else:
        print("Not connected to WiFi")
        redTripleFlashy()
        
        # try reconnect every 20 seconds
        utime.sleep(20)
        connect_to_wifi(ssid, password)
        utime.sleep(20)

    




