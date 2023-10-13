from machine import Pin
, ADC
import time

# Define the pin where your sensor is connected
sensor_pin = ADC(Pin('GP26'))


def check_rain(sensor):
    # Read the sensor value
    sensor_value = sensor.read_u16()

    # You may need to adjust the threshold based on your sensor and how you want to 
    # distinguish between rain and no rain.
    # Here, I am assuming that a higher reading means more rain, and I set the threshold arbitrarily.
    threshold = 50000
    print(sensor_value)
    if sensor_value > threshold:
        return True
    else:
        return False

print("starting")
while True:
    check_rain(sensor_pin)
    time.sleep(0.3)
    
    """
    if check_rain(sensor_pin):
        print("It's raining.")
    else:
        print("It's not raining.")

    # Sleep for a while before checking again
    time.sleep(1)
    """
