"""
Simple WiFi Connection Demo
This file demonstrates basic WiFi connection for educational purposes
"""
import network
import time
from secrets import secrets

# Connection configuration constants
MAX_WAIT_TIME = 10          # Maximum connection wait time in seconds  
CONNECTED_STATUS = 3        # WiFi connected status code
RETRY_INTERVAL = 1          # Time between connection checks

print("Starting WiFi connection demo...")
print(f"Attempting to connect to: {secrets['ssid']}")

# Initialize and activate WiFi interface
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Start connection attempt
wlan.connect(secrets['ssid'], secrets['password'])

# Monitor connection progress with timeout
remaining_time = MAX_WAIT_TIME
while remaining_time > 0:
    current_status = wlan.status()
    
    # Check if connection completed (success or failure)
    if current_status < 0 or current_status >= CONNECTED_STATUS:
        break
        
    remaining_time -= 1
    print(f"Establishing connection... {remaining_time}s remaining")
    time.sleep(RETRY_INTERVAL)

# Display connection result
if wlan.status() != CONNECTED_STATUS:
    print(f"ERROR: WiFi connection failed with status {wlan.status()}")
    raise RuntimeError("WiFi connection failed")
else:
    ip_address = wlan.ifconfig()[0]
    print("SUCCESS: WiFi connection established")
    print(f"Device IP Address: {ip_address}")
    print("Connection demo completed successfully")
