"""
CheerLights Global Color Synchronization
Simple project to sync LED colors worldwide
"""
import urequests
import json
import time
import machine
from ws2812 import WS2812
from do_connect import do_connect

# Simple configuration
LED_PIN = 0                    # LED strip data pin
LED_COUNT = 8                  # Number of LEDs  
UPDATE_INTERVAL = 10           # Update every 10 seconds
REQUEST_TIMEOUT = 10           # HTTP request timeout in seconds
API_URL = "http://api.thingspeak.com/channels/1417/field/2/last.json"

# Connect to WiFi and setup LEDs
print("Starting CheerLights...")
do_connect()
led_strip = WS2812(machine.Pin(LED_PIN), LED_COUNT)

def get_color():
    """Get current CheerLights color from internet with timeout protection"""
    response = None
    try:
        print("Getting new color...")
        
        # Make HTTP request with timeout
        response = urequests.get(API_URL, timeout=REQUEST_TIMEOUT)
        
        if response.status_code == 200:
            # Get color data from JSON
            data = json.loads(response.content.decode('utf-8'))
            hex_color = data['field2']
            print(f"New color: {hex_color}")
            
            # Convert hex to number (remove # symbol)
            color = int('0x' + hex_color[1:7], 16)
            return color
        else:
            print(f"HTTP error: status {response.status_code}")
            return None
            
    except OSError as e:
        print(f"Network error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
    finally:
        # Always close response to free resources
        if response:
            try:
                response.close()
            except:
                pass

# Main loop - runs forever with error recovery
print(f"Starting CheerLights! Updates every {UPDATE_INTERVAL} seconds")
consecutive_errors = 0
MAX_ERRORS = 3

while True:
    try:
        # Get the latest color from CheerLights
        color = get_color()
        
        # Update LEDs if we got a color
        if color is not None:
            led_strip.write_all(color)
            print("LEDs updated!")
            consecutive_errors = 0  # Reset error counter on success
        else:
            consecutive_errors += 1
            print(f"Failed to get color ({consecutive_errors}/{MAX_ERRORS})")
            
            # If too many consecutive errors, try to reconnect WiFi
            if consecutive_errors >= MAX_ERRORS:
                print("Too many errors, attempting WiFi reconnect...")
                try:
                    do_connect()
                    consecutive_errors = 0
                    print("WiFi reconnected successfully")
                except:
                    print("WiFi reconnect failed")
        
        # Wait before checking again
        print(f"Waiting {UPDATE_INTERVAL} seconds...")
        time.sleep(UPDATE_INTERVAL)
        
    except KeyboardInterrupt:
        print("CheerLights stopped by user")
        break
    except Exception as e:
        print(f"Main loop error: {e}")
        consecutive_errors += 1
        time.sleep(UPDATE_INTERVAL)
