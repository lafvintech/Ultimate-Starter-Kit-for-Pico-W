"""
Weather Station with LCD Display
Displays real-time weather information and local time on LCD screen
"""
import urequests
import time
import ntptime
from machine import I2C, Pin
from lcd1602 import LCD
from secrets import secrets
from do_connect import do_connect

# Hardware configuration constants
LCD_SDA_PIN = 6                # I2C SDA pin for LCD
LCD_SCL_PIN = 7                # I2C SCL pin for LCD  
I2C_FREQUENCY = 400000         # I2C bus frequency
I2C_BUS = 1                    # I2C bus number

# Display timing constants
LCD_CLEAR_DELAY = 200          # LCD clear delay in milliseconds
UPDATE_INTERVAL = 30           # Weather update interval in seconds
NTP_RETRY_DELAY = 2            # Delay between NTP sync attempts

# Weather API constants
DEFAULT_CITY = "Shenzhen"        # Default city for weather
DEFAULT_UNITS = "metric"       # Default measurement units
API_TIMEOUT = 10               # HTTP request timeout in seconds

print("Starting Weather Station...")

# Connect to WiFi
print("Connecting to WiFi...")
do_connect()

# Sync time with NTP server
print("Synchronizing time...")
ntp_attempts = 0
MAX_NTP_ATTEMPTS = 5

while ntp_attempts < MAX_NTP_ATTEMPTS:
    try:
        ntptime.settime()
        print("Time synchronized successfully")
        break
    except OSError as e:
        ntp_attempts += 1
        print(f"Time sync attempt {ntp_attempts}/{MAX_NTP_ATTEMPTS}...")
        time.sleep(NTP_RETRY_DELAY)

if ntp_attempts >= MAX_NTP_ATTEMPTS:
    print("WARNING: Time sync failed, using local time")

# Initialize LCD display
print(f"Initializing LCD on I2C bus {I2C_BUS}")
try:
    i2c = I2C(I2C_BUS, sda=Pin(LCD_SDA_PIN), scl=Pin(LCD_SCL_PIN), freq=I2C_FREQUENCY)
    lcd = LCD(i2c)
    lcd.clear()
    time.sleep_ms(LCD_CLEAR_DELAY)
    lcd.message("Weather Station\nInitializing...")
    print("LCD initialized successfully")
except Exception as e:
    print(f"ERROR: LCD initialization failed - {e}")
    raise

# OpenWeather API unit definitions
TEMPERATURE_UNITS = {
    "standard": "K",      # Kelvin
    "metric": "°C",       # Celsius  
    "imperial": "°F",     # Fahrenheit
}

SPEED_UNITS = {
    "standard": "m/s",    # Meters per second
    "metric": "m/s",      # Meters per second
    "imperial": "mph",    # Miles per hour
}

def get_weather_data(city=DEFAULT_CITY, api_key=None, units=DEFAULT_UNITS, lang='zh_cn'):
    """
    Fetch weather data from OpenWeatherMap API
    
    Args:
        city: City name for weather lookup
        api_key: OpenWeatherMap API key
        units: Measurement units (metric/imperial/standard)
        lang: Language for weather descriptions
    
    Returns:
        dict: Weather data or None if failed
    """
    if not api_key:
        print("ERROR: No API key provided")
        return None
        
    try:
        # Build API URL
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}&lang={lang}"
        print(f"Fetching weather for {city}...")
        
        # Make HTTP GET request with timeout
        response = urequests.get(url, timeout=API_TIMEOUT)
        
        if response.status_code == 200:
            weather_data = response.json()
            response.close()
            print("Weather data retrieved successfully")
            return weather_data
        else:
            print(f"API error: HTTP {response.status_code}")
            response.close()
            return None
            
    except OSError as e:
        print(f"Network error: {e}")
        return None
    except Exception as e:
        print(f"Weather fetch error: {e}")
        return None

def display_weather_debug(weather_data, units=DEFAULT_UNITS):
    """Print detailed weather information for debugging"""
    if not weather_data:
        print("No weather data to display")
        return
        
    try:
        timezone_hours = int(weather_data["timezone"] / 3600)
        sunrise = time.localtime(weather_data['sys']['sunrise'] + weather_data["timezone"])
        sunset = time.localtime(weather_data['sys']['sunset'] + weather_data["timezone"])
        
        print(f'=== Weather Details ===')
        print(f'City: {weather_data["name"]}, {weather_data["sys"]["country"]}')
        print(f'Coordinates: [{weather_data["coord"]["lon"]}, {weather_data["coord"]["lat"]}]')
        print(f'Timezone: UTC{timezone_hours:+d}')
        print(f'Sunrise: {sunrise[3]:02d}:{sunrise[4]:02d}')
        print(f'Sunset: {sunset[3]:02d}:{sunset[4]:02d}')
        print(f'Weather: {weather_data["weather"][0]["main"]}')
        print(f'Temperature: {weather_data["main"]["temp"]:.1f}{TEMPERATURE_UNITS[units]}')
        print(f'Feels like: {weather_data["main"]["feels_like"]:.1f}{TEMPERATURE_UNITS[units]}')
        print(f'Humidity: {weather_data["main"]["humidity"]}%')
        print(f'Pressure: {weather_data["main"]["pressure"]}hPa')
        
        if "wind" in weather_data:
            print(f'Wind: {weather_data["wind"]["speed"]}{SPEED_UNITS[units]}')
        if "visibility" in weather_data:
            print(f'Visibility: {weather_data["visibility"]}m')
            
    except KeyError as e:
        print(f"Missing weather data field: {e}")
    except Exception as e:
        print(f"Error displaying weather: {e}")

def update_lcd_display(lcd, weather_data, units=DEFAULT_UNITS):
    """Update LCD with current time and weather information"""
    try:
        if not weather_data:
            lcd.clear()
            lcd.message("Weather Station\nNo Data")
            return
            
        # Extract weather information
        weather_condition = weather_data["weather"][0]["main"]
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        
        # Calculate local time with timezone offset
        timezone_offset = int(weather_data["timezone"] / 3600)
        local_time = time.localtime()
        hours = (local_time[3] + timezone_offset) % 24
        minutes = local_time[4]
        
        # Format display strings
        line1 = f"{hours:02d}:{minutes:02d} {weather_condition}"
        line2 = f"{temperature:.1f}{TEMPERATURE_UNITS[units]} {humidity}%rh"
        
        # Update LCD display
        lcd.clear()
        time.sleep_ms(LCD_CLEAR_DELAY)
        lcd.message(f"{line1}\n{line2}")
        
        print(f"Display updated: {line1} | {line2}")
        
    except Exception as e:
        print(f"LCD update error: {e}")
        lcd.clear()
        lcd.message("Display Error\nCheck Connection")    


# Main weather monitoring loop
print("Starting weather monitoring...")
print(f"Update interval: {UPDATE_INTERVAL} seconds")

consecutive_errors = 0
MAX_ERRORS = 3

# Show loading message
lcd.clear()
lcd.message("Weather Station\nLoading...")

while True:
    try:
        # Fetch weather data
        weather_data = get_weather_data(
            city=DEFAULT_CITY,
            api_key=secrets['openweather_api_key'],
            units=DEFAULT_UNITS
        )
        
        if weather_data:
            # Update LCD display with weather info
            update_lcd_display(lcd, weather_data, DEFAULT_UNITS)
            
            # Reset error counter on success
            consecutive_errors = 0
            
            # Optional: Print detailed debug info (uncomment to enable)
            # display_weather_debug(weather_data, DEFAULT_UNITS)
            
        else:
            # Handle weather fetch failure
            consecutive_errors += 1
            print(f"Weather fetch failed ({consecutive_errors}/{MAX_ERRORS})")
            
            # Show error on LCD
            lcd.clear()
            lcd.message(f"Weather Error\nRetry {consecutive_errors}/{MAX_ERRORS}")
            
            # Try to reconnect WiFi after multiple failures
            if consecutive_errors >= MAX_ERRORS:
                print("Too many consecutive errors, attempting WiFi reconnect...")
                try:
                    do_connect()
                    consecutive_errors = 0
                    print("WiFi reconnected successfully")
                    lcd.clear()
                    lcd.message("WiFi Reconnected\nResuming...")
                    time.sleep(2)
                except Exception as e:
                    print(f"WiFi reconnect failed: {e}")
        
        # Wait before next update
        print(f"Next update in {UPDATE_INTERVAL} seconds...")
        time.sleep(UPDATE_INTERVAL)
        
    except KeyboardInterrupt:
        print("Weather station stopped by user")
        lcd.clear()
        lcd.message("Weather Station\nStopped")
        break
        
    except Exception as e:
        print(f"Unexpected error in main loop: {e}")
        consecutive_errors += 1
        lcd.clear()
        lcd.message("System Error\nCheck Console")
        time.sleep(UPDATE_INTERVAL)
