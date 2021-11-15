import Adafruit_DHT as DHT #sudo pip3 install Adafruit_DHT
from firebase import firebase #sudo pip3 install python-firebase
import csv
import requests, json
import time
import random
from time import sleep
from datetime import datetime
import pibrella as pb
import sys

roomNumber = 14


# for startup code:
# sudo nano /etc/rc.local
# sudo python3/home/pi/r5.py &

def getOutSideTemp():
    api_key = "a19c355c905cbcb821b784d45a9cb1de"

    # base_url variable to store url 
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    # Give city name 
    # city_name = input("Enter city name : ")
    city_name = "rush"

    # complete_url variable to store 
    # complete url address 
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name 

    # get method of requests module 
    # return response object 
    response = requests.get(complete_url) 

    # json method of response object 
    # convert json format data into 
    # python format data 
    x = response.json()
    #print(x)

    # Now x contains list of nested dictionaries 
    # Check the value of "cod" key is equal to 
    # "404", means city is found otherwise, 
    # city is not found 
    if x["cod"] != "404": 

        # store the value of "main"
        # key in variable y 
        y = x["main"] 

        # store the value corresponding 
        # to the "temp" key of y 
        current_temperature = round(y["temp"]-273.15,2)


        current_pressure = y["pressure"]
        # store the value of "weather"
        # key in variable z
        
        # store the value corresponding 
        # to the "humidity" key of y 
        current_humidiy = y["humidity"]  


        # print following values 
        print("Temp Outdoors:" + str(current_temperature) + " °C", end = " / ")


    else:   
          print(" City Not Found ")
    
    return current_temperature

def readLocalTemp():
    sensor = DHT.DHT11
    pin = 26
    
    while True:

        dhtHumidity, dhtTemperature = DHT.read(sensor, pin)
        
        if dhtHumidity is not None and dhtTemperature is not None:

        #print(dhtHumidity)
            print("Temp Indoors:", dhtTemperature, "°C", end = " / ")
            return dhtTemperature
            break
        else:
            print(".", end ="") #error reading DHT but so common we'll just make it a dot and try again
        


#######################################################################################indoor temperature test
def writeTempToCSV(temperatureForCSV):
    f= open("covid19.csv", "w" , newline="")

    wc=csv.writer(f)

    wc.writerow(["Temperature Difference"]),wc.writerow([temperatureForCSV])
    #wc.writerow(["humidityForCSV"]),wc.writerow([humi])
        
    f.close()


def button_changed(pin):
    if pin.read() ==1:
        print("YOU JUST HAD TO PUSH THAT BUTTON")
        sleep(1)
        sys.exit(0)

#check difference
    
firebase = firebase.FirebaseApplication('https://rpitempdata.firebaseio.com/', None)
########################################################
try:
    pb.buzzer.buzz(1000)
    sleep(0.2)
    pb.buzzer.buzz(5000)
    sleep(0.2)
    pb.buzzer.off()
    
    
    while True:
        # roomNumber = input("Type in your Room Number")

        #gets the times and dates now
        pb.output.e.write(1)
        
        now = datetime.now()
        timeNow = now.strftime("%H:%M:%S") 
        dateNow = now.strftime("%d:%m:%Y")
        
        print(timeNow,dateNow, end = " | ")
        
        localTempReading = readLocalTemp()
        outsideTempDownload = getOutSideTemp()

        tempDifference = round(localTempReading - outsideTempDownload)
        print("Temp Difference is:", tempDifference, "°C")
        
        pb.lights.off()
        
        if tempDifference < 8:
            pb.light.green.on()
            
        elif tempDifference >8 and tempDifference < 10:
            pb.light.yellow.on()
            
        elif tempDifference >10 and tempDifference < 26:
            pb.light.red.on()
        
        else:
            pb.light.red.pulse(0,0,1,1)
            
            pb.buzzer.buzz(20000)
            sleep(1)
            pb.buzzer.fail()
        

            

        # write data to csv
        writeTempToCSV(tempDifference)

        
            # attatches names to the data
        data = {"TempDifference": tempDifference, "LocalTemp": localTempReading,"OutsideTemp": outsideTempDownload, "TimeStamp": timeNow , "DateStamp": dateNow   }
            
            #POSTS  to the database (POST means create an entry, does generate a nasty long node name)
        firebase.post('/R'+str(roomNumber), data)
        
        pb.output.e.write(0)
        
        # wait: uses output leds as countdown lights
        for x in range(50): # 3600 is 1 hour, 900 is 15 nubs
            pb.output.f.write(1)
            sleep(0.33)
            pb.output.g.write(1)
            sleep(0.33)
            pb.output.h.write(1)
            sleep(0.33)
            pb.outputs.off()
            
            # Abort program button check if pressed
            if pb.button.read()==1:
                print("Button Press Exit")
                sys.exit()
                break
except:
    print("Shutting down")
    pb.outputs.off
    pb.lights.off()
    
    # power down noise
    pb.buzzer.buzz(5000)
    sleep(0.2)
    pb.buzzer.buzz(1000)
    sleep(0.2)
    pb.buzzer.off()