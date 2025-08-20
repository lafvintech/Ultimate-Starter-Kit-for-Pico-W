import network
import time
from secrets import secrets

# WiFi connection constants
WIFI_CONNECTION_TIMEOUT = 10    # Maximum wait time in seconds
WIFI_STATUS_CONNECTED = 3       # WiFi connected status code
WIFI_STATUS_ERROR_MIN = 0       # Minimum error status code
CONNECTION_RETRY_DELAY = 1      # Delay between connection attempts

def do_connect(ssid=secrets['ssid'], psk=secrets['password'], timeout=WIFI_CONNECTION_TIMEOUT):
    """
    Connect to WiFi network with improved error handling
    
    Args:
        ssid: WiFi network name
        psk: WiFi password
        timeout: Connection timeout in seconds
    
    Returns:
        str: IP address if successful
        
    Raises:
        RuntimeError: If connection fails
    """
    print(f"Connecting to WiFi network: {ssid}")
    
    # Initialize WiFi interface
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    # Attempt connection
    wlan.connect(ssid, psk)

    # Wait for connection with timeout
    wait_time = timeout
    while wait_time > 0:
        status = wlan.status()
        if status < WIFI_STATUS_ERROR_MIN or status >= WIFI_STATUS_CONNECTED:
            break
        wait_time -= 1
        print(f"Waiting for connection... ({wait_time}s remaining)")
        time.sleep(CONNECTION_RETRY_DELAY)

    # Check connection result
    if wlan.status() != WIFI_STATUS_CONNECTED:
        error_msg = f"WiFi connection failed. Status: {wlan.status()}"
        print(f"ERROR: {error_msg}")
        raise RuntimeError(error_msg)
    else:
        ip_address = wlan.ifconfig()[0]
        print(f"WiFi connected successfully!")
        print(f"IP Address: {ip_address}")
        return ip_address
