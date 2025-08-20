"""
Blynk Smart Environmental Control System
MicroPython version with DHT11 sensor and RGB LED control

This program connects to Blynk IoT platform and provides:
- Environmental monitoring (temperature & humidity)
- RGB LED control via mobile app
- Real-time sensor data updates

Hardware Requirements:
- ESP32/ESP8266 with MicroPython
- DHT11 sensor connected to GPIO 16
- RGB LEDs: Red(GPIO 13), Green(GPIO 14), Blue(GPIO 15)

Blynk Virtual Pin Setup:
- V0: Red LED brightness (Slider 0-100)
- V1: Green LED brightness (Slider 0-100)  
- V2: Blue LED brightness (Slider 0-100)
- V3: Temperature display (Value Display)
- V4: Humidity display (Value Display)

Setup Requirements:
1. Create account at blynk.cloud
2. Create new template and device
3. Add virtual pins V0-V4 with appropriate widgets
4. Copy device auth token
5. Configure BLYNK_TOKEN below
"""

import time
import machine
import urequests as requests
from machine import Pin, PWM
from do_connect import do_connect
from dht import DHT11, InvalidPulseCount

# =====================================
# Configuration (modify as needed)
# =====================================
BLYNK_TOKEN = "YOUR_BLYNK_TOKEN_HERE"  # Replace with your actual token from blynk.cloud

# Hardware pin configuration (matching 4.web_page.py)
RED_LED_PIN = 13        # Red LED GPIO pin
GREEN_LED_PIN = 14      # Green LED GPIO pin  
BLUE_LED_PIN = 15       # Blue LED GPIO pin
DHT_SENSOR_PIN = 16     # DHT11 sensor data pin

# Sensor configuration
SENSOR_RETRY_COUNT = 3         # Retry attempts for failed sensor readings
SENSOR_UPDATE_INTERVAL = 10    # Send sensor data every 10 seconds
CONTROL_CHECK_INTERVAL = 1     # Check control commands every 1 second

# =====================================
# Hardware Initialization
# =====================================

# Initialize RGB LEDs with PWM for brightness control
print("Setting up RGB LED PWM pins...")
red_led = PWM(Pin(RED_LED_PIN))
green_led = PWM(Pin(GREEN_LED_PIN))
blue_led = PWM(Pin(BLUE_LED_PIN))

# Set PWM frequency (1000 Hz is good for LEDs)
red_led.freq(1000)
green_led.freq(1000)
blue_led.freq(1000)

# Turn off all LEDs initially (0% brightness)
red_led.duty_u16(0)
green_led.duty_u16(0)
blue_led.duty_u16(0)

# Initialize DHT11 sensor
print(f"Initializing DHT11 sensor on pin {DHT_SENSOR_PIN}")
sensor_pin = Pin(DHT_SENSOR_PIN, Pin.IN)
dht_sensor = DHT11(sensor_pin)

# =====================================
# Blynk API Functions
# =====================================

def blynk_write(token, pin, value):
    """
    Write value to Blynk virtual pin
    
    Args:
        token: Blynk authentication token
        pin: Virtual pin name (e.g., "V0")
        value: Value to write
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        api_url = f"https://blynk.cloud/external/api/update?token={token}&{pin}={value}"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            print(f"✓ Successfully updated {pin} = {value}")
            response.close()
            return True
        else:
            print(f"❌ Failed to update {pin}. Status: {response.status_code}")
            response.close()
            return False
            
    except Exception as e:
        print(f"❌ Error writing to Blynk: {e}")
        return False

def blynk_read(token, pin):
    """
    Read value from Blynk virtual pin
    
    Args:
        token: Blynk authentication token
        pin: Virtual pin name (e.g., "V0")
    
    Returns:
        str: Pin value or None if error
    """
    try:
        api_url = f"https://blynk.cloud/external/api/get?token={token}&{pin}"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            value = response.text.strip()
            response.close()
            return value
        else:
            print(f"❌ Failed to read {pin}. Status: {response.status_code}")
            response.close()
            return None
            
    except Exception as e:
        print(f"❌ Error reading from Blynk: {e}")
        return None

# =====================================
# Sensor Functions
# =====================================

def read_sensor_data():
    """
    Read temperature and humidity from DHT11 sensor with retry logic
    
    Returns:
        tuple: (temperature, humidity) or (None, None) if failed
    """
    for attempt in range(SENSOR_RETRY_COUNT):
        try:
            dht_sensor.measure()
            temperature = dht_sensor.temperature
            humidity = dht_sensor.humidity
            
            # Validate sensor readings
            if temperature is not None and humidity is not None:
                print(f"📊 Sensor reading: {temperature}°C, {humidity}%")
                return temperature, humidity
            else:
                print(f"⚠️  Invalid sensor reading on attempt {attempt + 1}")
                
        except (OSError, InvalidPulseCount) as e:
            print(f"⚠️  Sensor read attempt {attempt + 1} failed: {e}")
            
        except Exception as e:
            print(f"❌ Unexpected sensor error on attempt {attempt + 1}: {e}")
            
        # Small delay before retry
        if attempt < SENSOR_RETRY_COUNT - 1:
            time.sleep(0.1)
    
    print("❌ All sensor read attempts failed")
    return None, None

# =====================================
# RGB LED Control Functions
# =====================================

def brightness_to_pwm(brightness_percent):
    """
    Convert brightness percentage (0-100) to PWM duty cycle (0-65535)
    
    Args:
        brightness_percent: Brightness value from 0-100
        
    Returns:
        int: PWM duty cycle value (0-65535)
    """
    if brightness_percent < 0:
        brightness_percent = 0
    elif brightness_percent > 100:
        brightness_percent = 100
    
    # Map 0-100 to 0-65535
    return int((brightness_percent / 100.0) * 65535)

def set_rgb_brightness(red_brightness=0, green_brightness=0, blue_brightness=0):
    """
    Set RGB LED brightness using PWM control
    
    Args:
        red_brightness: Red LED brightness (0-100)
        green_brightness: Green LED brightness (0-100)
        blue_brightness: Blue LED brightness (0-100)
    """
    # Convert percentages to PWM values
    red_pwm = brightness_to_pwm(red_brightness)
    green_pwm = brightness_to_pwm(green_brightness)
    blue_pwm = brightness_to_pwm(blue_brightness)
    
    # Set PWM duty cycles
    red_led.duty_u16(red_pwm)
    green_led.duty_u16(green_pwm)
    blue_led.duty_u16(blue_pwm)
    
    # Display status
    active_colors = []
    if red_brightness > 0:
        active_colors.append(f"Red({red_brightness}%)")
    if green_brightness > 0:
        active_colors.append(f"Green({green_brightness}%)")
    if blue_brightness > 0:
        active_colors.append(f"Blue({blue_brightness}%)")
    
    if active_colors:
        print(f"🌈 RGB LEDs: {', '.join(active_colors)}")
    else:
        print("💡 All RGB LEDs: OFF (0%)")

def turn_off_all_leds():
    """Turn off all RGB LEDs (set brightness to 0%)"""
    red_led.duty_u16(0)
    green_led.duty_u16(0)
    blue_led.duty_u16(0)
    print("💡 All RGB LEDs turned OFF (0%)")

# =====================================
# Main Program
# =====================================

def main():
    """Main program loop for Smart Environmental Control System"""
    
    print("🚀 Starting Blynk Smart Environmental Control System")
    print("=" * 55)
    
    # Check configuration
    if BLYNK_TOKEN == "YOUR_BLYNK_TOKEN_HERE":
        print("❌ ERROR: Please configure your BLYNK_TOKEN")
        print("   Get your token from: https://blynk.cloud")
        print("   Edit this file and replace BLYNK_TOKEN value")
        return
    
    # Connect to WiFi
    print("📶 Connecting to WiFi...")
    try:
        do_connect()
        print("✓ WiFi connected successfully")
    except Exception as e:
        print(f"❌ WiFi connection failed: {e}")
        return
    
    print("🏠 Smart Environmental Control System Ready!")
    print(f"🔑 Using token: {BLYNK_TOKEN[:8]}...")
    print("📊 DHT11 sensor monitoring temperature & humidity")
    print("🔴🟢🔵 RGB LEDs controlled via Blynk app")
    print("📱 Virtual Pins: V0=Red, V1=Green, V2=Blue, V3=Temp, V4=Hum")
    print("⏹️  Press Ctrl+C to exit")
    print("-" * 55)
    
    # Initialize state tracking for RGB brightness values
    previous_rgb_brightness = {"red": None, "green": None, "blue": None}
    last_sensor_update = 0
    error_count = 0
    max_errors = 5
    
    try:
        while True:
            current_time = time.time()
            
            try:
                # ===== Control RGB LEDs based on Blynk slider values =====
                
                # Read RGB brightness sliders (0-100)
                red_brightness = blynk_read(BLYNK_TOKEN, "V0")
                green_brightness = blynk_read(BLYNK_TOKEN, "V1") 
                blue_brightness = blynk_read(BLYNK_TOKEN, "V2")
                
                # Process RGB brightness controls
                rgb_changed = False
                
                # Check for brightness changes
                if red_brightness != previous_rgb_brightness["red"] and red_brightness is not None:
                    previous_rgb_brightness["red"] = red_brightness
                    rgb_changed = True
                
                if green_brightness != previous_rgb_brightness["green"] and green_brightness is not None:
                    previous_rgb_brightness["green"] = green_brightness  
                    rgb_changed = True
                    
                if blue_brightness != previous_rgb_brightness["blue"] and blue_brightness is not None:
                    previous_rgb_brightness["blue"] = blue_brightness
                    rgb_changed = True
                
                # Update RGB LEDs if any brightness changed
                if rgb_changed:
                    try:
                        # Convert string values to integers
                        red_val = int(red_brightness) if red_brightness is not None else 0
                        green_val = int(green_brightness) if green_brightness is not None else 0
                        blue_val = int(blue_brightness) if blue_brightness is not None else 0
                        
                        # Set LED brightness
                        set_rgb_brightness(red_val, green_val, blue_val)
                        
                    except ValueError as e:
                        print(f"⚠️  Invalid brightness value: {e}")
                        # Set to safe default values
                        set_rgb_brightness(0, 0, 0)
                
                # ===== Read and Send Sensor Data =====
                
                # Send sensor data every SENSOR_UPDATE_INTERVAL seconds
                if current_time - last_sensor_update >= SENSOR_UPDATE_INTERVAL:
                    temperature, humidity = read_sensor_data()
                    
                    if temperature is not None and humidity is not None:
                        # Send temperature and humidity to Blynk
                        temp_success = blynk_write(BLYNK_TOKEN, "V3", str(temperature))
                        hum_success = blynk_write(BLYNK_TOKEN, "V4", str(humidity))
                        
                        if temp_success and hum_success:
                            print(f"✅ Sensor data sent: {temperature}°C, {humidity}%")
                        else:
                            print("⚠️  Failed to send sensor data to Blynk")
                    else:
                        # Send error values to Blynk
                        blynk_write(BLYNK_TOKEN, "V3", "Error")
                        blynk_write(BLYNK_TOKEN, "V4", "Error")
                        print("❌ Sensor error - sent error values to Blynk")
                    
                    last_sensor_update = current_time
                
                # Reset error count on successful operation
                error_count = 0
                
                # Wait before next control check
                time.sleep(CONTROL_CHECK_INTERVAL)
                
            except KeyboardInterrupt:
                print("\n🛑 Program stopped by user")
                break
                
            except Exception as e:
                print(f"❌ Loop error: {e}")
                error_count += 1
                
                if error_count >= max_errors:
                    print("❌ Too many errors. Restarting device...")
                    time.sleep(2)
                    machine.reset()
                else:
                    time.sleep(2)  # Wait before retry
    
    except Exception as e:
        print(f"❌ Fatal error: {e}")
    
    finally:
        # Cleanup
        print("🧹 Cleaning up...")
        turn_off_all_leds()  # Sets all RGB LEDs to 0% brightness
        print("✓ Hardware cleanup completed")

# =====================================
# Program Entry Point
# =====================================

if __name__ == "__main__":
    main()
