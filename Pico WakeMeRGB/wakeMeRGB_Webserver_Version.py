import network
import time
import utime
import ntptime
import urequests

import socket
from machine import Pin

from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine



ssid = 'x'
password = 'x'

# internal led
led = machine.Pin("LED", machine.Pin.OUT)
led.on()

pinIn = Pin(17, Pin.IN,Pin.PULL_UP)
button_check_period = 100
timeout_period = 0.2
last_time_stamp = "Updating Soon"
    
    
def get_time():
    response = urequests.get("http://worldtimeapi.org/api/timezone/Europe/London")
    json_data = response.json()
    datetime_str = json_data['datetime']  # format: "2023-11-01T12:34:56.789123+00:00"
    hour = int(datetime_str[11:13])
    return hour

def get_longer_time():
    response = urequests.get("http://worldtimeapi.org/api/timezone/Europe/London")
    json_data = response.json()
    datetime_str = json_data['datetime']  # format: "2023-11-01T12:34:56.789123+00:00"
    print(datetime_str)
    full_time = datetime_str
    return full_time


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


def quickflashInteralLED():
    for x in range(2):
        led.on()
        utime.sleep(0.1)
        led.off()
        utime.sleep(0.1)



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


def open_socket(ip):
    # Open a socket
    print("opening a socket at")
    address = (ip, 80)
    print(address)
    connection = socket.socket()
    #connection.settimeout(timeout_period)
    connection.bind(address)
    connection.listen(5)
    print("Connection is", connection)
    return connection



def webpage(temperature, state, last_time_stamp):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <img id="mainImage" src="https://cdn.glitch.global/b2cfa0c1-97f8-4a83-965e-626eb3389485/wakeme.png?v=1698946267231" width="200" alt="Colorful Image"/>
            <form action="./lighton">
            <input type="submit" value="Light on" />
            </form>
            <form action="./lightoff">
            <input type="submit" value="Light off" />
            </form>
            <form action="./rainbow">
            <input type="submit" value="RAINBOWTIME" />
            </form>
            <p>LED is {state}</p>
            <p>Temperature is {temperature}</p>
            <p>Last Online {last_time_stamp}</p>
            </body>
            </html>
            """
    return str(html)

def serve(connection):
    #Start a web server
    state = 'OFF'
    pico_led.off()
    temperature = 0
    
    while True:
        
        
        
        print("Starting while loop")
         
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        print("Request is", request)
        try:
            request = request.split()[1]
            print("next is", request)
        except IndexError:
            pass
        
        if request == '/lighton?':
            pico_led.on()
            state = 'ON'
            
        elif request =='/lightoff?':
            pico_led.off()
            state = 'OFF'
         
        elif request =='/rainbow?':
            bootup_colour_rainbow()
            print("REMOTE RAINBOW REQUESTED!")
        
        
        
        temperature = pico_temp_sensor.temp
        #last_timestamp = 10
        
        # update webpage
        print("updating webpage")
        
        last_time_stamp=get_longer_time()
        html = webpage(temperature, state, last_time_stamp)
        client.send(html)
        client.close()
    
    
        print("Socket Timed Out")
            
        print("Waiting for button push")
        for x in range(button_check_period):
            
            if pinIn.value():
                print(".", end=" ")
            else:
                print("BUTTON PUSH DETECTED! RAINBOW REQUEST!")
                bootup_colour_rainbow()
            
            
            utime.sleep(0.1)
        
        
        
        
        print("Checking time for colour")
        if network.WLAN(network.STA_IF).isconnected():
            flashInteralLED()
            hour = get_time()
            
            print("Current time: {}:00".format(hour))
            print("That is", hour)
            
            if hour >= 19 and hour <= 24:
                print("Red for Bed")
                red()
                
            elif hour >= 0 and hour < 7:
                print("Red for Bed")
                red()
                
            elif hour >= 7 and hour < 8:
                print("Good morning Green for getting up")
                green()
                
            elif hour >= 8 and hour < 18:
                print("Day Time Blue")
                blue()
                
            elif hour >= 18 and hour < 19:
                print("Ready for bed purple")
                purple()
            else:
                print("???")
                blueGreen()
            
            
            
        else:
            print("Not connected to WiFi")
            redTripleFlashy()



def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        quickflashInteralLED()
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

    
# start

print("Starting up")

flashInteralLED()

while True:

    try:
        ip = connect()
        connection = open_socket(ip)
        serve(connection)
        
        
    except KeyboardInterrupt:
        machine.reset()
        



    





