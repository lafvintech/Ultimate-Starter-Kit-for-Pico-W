from lcd1602 import LCD
from machine import I2C, Pin
import utime as time
from dht import DHT11, InvalidPulseCount

# Initialize DHT11 and LCD
sensor = DHT11(Pin(16, Pin.IN, Pin.PULL_UP))  # Connect DHT11 to GPIO16
i2c = I2C(1, sda=Pin(6), scl=Pin(7), freq=400000)
lcd = LCD(i2c)

def read_sensor():
    """Read data from the DHT11 sensor"""
    try:
        sensor.measure()
        temp = sensor.temperature
        hum = sensor.humidity
        return temp, hum
    except InvalidPulseCount:
        print('Invalid pulse count - retrying...')
        return None, None
    except Exception as e:
        print('Error reading sensor:', e)
        return None, None

# Main loop
while True:
    temp, hum = read_sensor()
    if temp is not None and hum is not None:
        # Display temperature and humidity
        string = "Temp: {:.1f}C\nHumi: {:.1f}%".format(temp, hum)
        lcd.message(string)
    else:
        lcd.message("Sensor Error\nPlease wait...")

    time.sleep(2)  # DHT11 recommends a sampling interval of at least 2 seconds
    lcd.clear()
