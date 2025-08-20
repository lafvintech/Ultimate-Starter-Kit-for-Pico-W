# 6.7_led_bar_level.py
# Description: A digital spirit level using an MPU6050 sensor and a 10-segment LED bar graph.
# The lit LED on the bar indicates the angle of tilt.

import machine
from machine import I2C, Pin
import time
import math
from imu import MPU6050

# --- Hardware Configuration ---

# 1. MPU6050 (GY-521) Sensor Setup
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
mpu = MPU6050(i2c)
print("MPU6050 sensor initialized.")

# 2. LED Bar Setup (using pins from the chaser light project)
LED_PINS = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
NUM_LEDS = len(LED_PINS)
leds = []

# --- Helper Functions ---

def initialize_leds():
    """Initialize all LED pins as outputs and store them."""
    global leds
    for pin_id in LED_PINS:
        led = machine.Pin(pin_id, machine.Pin.OUT)
        led.value(0)  # Ensure all LEDs are off initially
        leds.append(led)
    print(f"Initialized {NUM_LEDS}-segment LED bar.")

def dist(a, b):
    """Calculates the distance between two points, used for angle calculation."""
    return math.sqrt((a * a) + (b * b))

def get_x_rotation(x, y, z):
    """Calculates the rotation angle around the X-axis from accelerometer data."""
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)

def map_value(x, in_min, in_max, out_min, out_max):
    """Maps a value from one numerical range to another."""
    # Clamp the input value to the specified range
    x = max(in_min, min(x, in_max))
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# --- Core Logic ---

def update_led_bar_display(angle):
    """Updates the LED bar to reflect the current tilt angle."""
    
    # Define the sensitivity range. A smaller angle range makes the level more sensitive.
    # e.g., -30 to +30 degrees of tilt will cover the full LED bar.
    SENSITIVITY_RANGE = 30.0
    
    # Map the angle (-SENSITIVITY_RANGE to +SENSITIVITY_RANGE) to an LED index (0 to 9)
    led_index = map_value(angle, -SENSITIVITY_RANGE, SENSITIVITY_RANGE, 0, NUM_LEDS - 1)
    led_index = int(round(led_index))
    
    # Turn all LEDs off, then turn the correct one on.
    for i in range(NUM_LEDS):
        if i == led_index:
            leds[i].value(1)  # Turn on the target LED
        else:
            leds[i].value(0)  # Turn off all other LEDs

# --- Main Program ---

def main():
    """Main function to run the digital level."""
    
    initialize_leds()
    
    print("\nDigital Level is active. Tilt the sensor.")
    print("The middle LED indicates a level surface.")
    
    try:
        while True:
            # Read accelerometer data from the sensor
            accel_data = mpu.accel
            
            # Calculate the tilt angle
            x_angle = get_x_rotation(accel_data.x, accel_data.y, accel_data.z)
            
            # Update the LED display based on the angle
            update_led_bar_display(x_angle)
            
            # Optional: print the angle for debugging
            # print(f"Angle: {x_angle:.2f} degrees")
            
            # A short delay to keep the updates smooth
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        print("\nProgram stopped by user.")
    finally:
        # Ensure all LEDs are turned off on exit
        for led in leds:
            led.value(0)
        print("All LEDs turned off. Goodbye!")

# Run the main program
if __name__ == "__main__":
    main() 