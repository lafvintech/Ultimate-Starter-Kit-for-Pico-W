# WiFi and API Configuration
# Modify these values according to your network and service requirements

# Network configuration constants
DEFAULT_WIFI_SSID = 'your-wifi-ssid'
DEFAULT_WIFI_PASSWORD = 'your-wifi-password'
OPENWEATHER_API_KEY = 'your-openweather-api-key'

# Configuration dictionary for backward compatibility
secrets = {
    'ssid': DEFAULT_WIFI_SSID,           # Your WiFi network name
    'password': DEFAULT_WIFI_PASSWORD,   # Your WiFi password  
    'openweather_api_key': OPENWEATHER_API_KEY  # OpenWeather API key
}

def validate_wifi_config():
    """Validate WiFi configuration settings"""
    if not secrets['ssid'] or not secrets['password']:
        print("ERROR: WiFi credentials not configured properly")
        return False
    if len(secrets['ssid']) == 0 or len(secrets['password']) < 8:
        print("WARNING: Check WiFi credentials format")
        return False
    print("WiFi configuration validated successfully")
    return True

def validate_api_config():
    """Validate API configuration settings"""
    if not secrets['openweather_api_key']:
        print("WARNING: OpenWeather API key not configured")
        return False
    if len(secrets['openweather_api_key']) != 32:
        print("WARNING: OpenWeather API key format may be incorrect")
        return False
    print("API configuration validated successfully")  
    return True