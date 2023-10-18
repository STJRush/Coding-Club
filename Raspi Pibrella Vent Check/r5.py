import Adafruit_DHT as DHT #sudo pip3 install Adafruit_DHT
from firebase import firebase #sudo pip3 install python-firebase
import csv
import requests, json
import time
import random
from time import sleep
from datetime import datetime

roomNumber = 5

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
        print("Outdoor Temperature = " + str(current_temperature) + " °C")


    else:   
          print(" City Not Found ")
    
    return current_temperature

def readLocalTemp():
    sensor = DHT.DHT11
    pin = 4
    
    while True:

        dhtHumidity, dhtTemperature = DHT.read(sensor, pin)
        
        if dhtHumidity is not None and dhtTemperature is not None:

        #print(dhtHumidity)
            print("Indoor Temperature is:", dhtTemperature, "°C")
            return dhtTemperature
            break
        else:
            print("DHT Error, let me try again")
        


#######################################################################################indoor temperature test
def writeTempToCSV(temperatureForCSV):
    f= open("covid19.csv", "w" , newline="")

    wc=csv.writer(f)

    wc.writerow(["Temperature Difference"]),wc.writerow([temperatureForCSV])
    #wc.writerow(["humidityForCSV"]),wc.writerow([humi])
        
    f.close()

#check difference
########################################################
while True:
    
    # roomNumber = input("Type in your Room Number")

    #gets the times and dates now
    now = datetime.now()
    timeNow = now.strftime("%H:%M:%S") 
    dateNow = now.strftime("%d:%m:%Y") 

    localTempReading = readLocalTemp()
    outsideTempDownload = getOutSideTemp()

    tempDifference = localTempReading - outsideTempDownload
    print("Temp Difference is:", tempDifference, "°C")

    # write data to csv
    writeTempToCSV(tempDifference)

    firebase = firebase.FirebaseApplication('https://rpitempdata.firebaseio.com/', None)
        # attatches names to the data
    data = {"TempDifference": tempDifference, "LocalTemp": localTempReading,"OutsideTemp": outsideTempDownload, "TimeStamp": timeNow , "DateStamp": dateNow   }
        
        #POSTS  to the database (POST means create an entry, does generate a nasty long node name)
    firebase.post('/R'+str(roomNumber), data)

    sleep(300)
