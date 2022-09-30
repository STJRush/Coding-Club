# Python program to test
from pygame import mixer # For sound effects
from time import sleep

# Starting the mixer
mixer.init()

# internet speed test
import speedtest
import statistics

swanLakePlayingFlag = False
while True:
    try:
        st = speedtest.Speedtest()
        
        listOfTestSpeeds=[]
        for testNo in range(3):
            speedResult = st.download()//1000000 # gets speed in Mbps
            print("Download Speed Test No.",testNo,speedResult,"Mbps")
            listOfTestSpeeds.append(speedResult)

        averageExternalInternetSpeed = round(int(statistics.mean(listOfTestSpeeds)))
        print("----> Average Download speed is", averageExternalInternetSpeed,"Mbps")
        
        if averageExternalInternetSpeed < 50:
            print("The whole internet is really bad")         
        elif averageExternalInternetSpeed < 100:
            print("External internet not great, not terrible.")
        elif averageExternalInternetSpeed > 100 and averageExternalInternetSpeed < 190:
            print("External internet is doing okay ")
        elif averageExternalInternetSpeed > 190:
            print("External internet is doing great! Good internet yay!")
        else:
            print("WTF")
        print("")
        swanLakePlayingFlag = False
        
    except:
        print("Internet is completely down")
        
        if swanLakePlayingFlag is False:
            mixer.music.load("swanLakeMoscow.mp3")
            mixer.music.play()
            swanLakePlayingFlag = True
        
