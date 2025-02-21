import os
import ipaddress
import wifi
import socketpool
import time
import microcontroller
import board
import digitalio
import simpleio
import adafruit_requests
import ssl
import random

# Get wifi and blynk token details from a settings.toml file
ssid = os.getenv("CIRCUITPY_WIFI_SSID")
password = os.getenv("CIRCUITPY_WIFI_PASSWORD")
blynkToken = os.getenv("blynk_auth_token")

# Buzzer
NOTE_C5 = 523
buzzer = board.GP18

# Initialize LED and button.
led = digitalio.DigitalInOut(board.GP1)
led.direction = digitalio.Direction.OUTPUT

# Variable to store the previous button value
previous_button = None  


# Write API
def write(token,pin,value):
        api_url = "https://blynk.cloud/external/api/update?token="+token+"&"+pin+"="+value
        response = requests.get(api_url)
        if "200" in str(response):
                print("Value successfully updated")
        else:
                print("Could not find the device token or wrong pin format")
# Read API
def read(token,pin):
        api_url = "https://blynk.cloud/external/api/get?token="+token+"&"+pin
        response = requests.get(api_url)
        return response.content.decode()
    
# Connect to Wi-Fi AP
print(f"Initializing...")
wifi.radio.connect(ssid, password)
print("connected!\n")
pool = socketpool.SocketPool(wifi.radio)
print("IP Address: {}".format(wifi.radio.ipv4_address))
print("Connecting to WiFi '{}' ...\n".format(ssid), end="")
requests = adafruit_requests.Session(pool, ssl.create_default_context())

simpleio.tone(buzzer, NOTE_C5, duration=0.1)


while True:
    try:
        while not wifi.radio.ipv4_address or "0.0.0.0" in repr(wifi.radio.ipv4_address):
            print("Reconnecting to WiFi...")
            wifi.radio.connect(ssid, password)

        # Read Blynk virtual pin V0
        # V0 can be assigned to Button Widget on Blynk App
        button = read(blynkToken, "V0")
        
        if button != previous_button:
            # The statement has changed
            print(f"Button state changed: {button}")
            simpleio.tone(buzzer, NOTE_C5, duration=0.1)
            previous_button = button

        if button == "1":
            led.value = True
            
        else:
            led.value = False


    except OSError as e:
        print("Failed!\n", e)
        microcontroller.reset()