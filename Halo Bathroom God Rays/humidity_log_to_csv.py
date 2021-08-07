from time import sleep
import Adafruit_DHT as DHT
import csv

def get_humidity():
    humid, temp = DHT.read_retry(DHT.DHT11, 3)
    print(temp, humid)
    
    return humid


######## Takes 200 reading from sensor and writes them to a .csv #########
try:
    f = open("humidityLog.csv", "w", newline="") #give your .csv file a name
    rc=csv.writer(f)                           

    rc.writerow(["Humidity"])      #start with a heading

    #run for about 33 mins (200 loops)

    for x in range(200):                       
        rc. writerow([get_humidity()])     
        sleep(10)

finally:
    f.close()                                  #close the file when done to prevent data loss
    print("All done! Closed safely")
