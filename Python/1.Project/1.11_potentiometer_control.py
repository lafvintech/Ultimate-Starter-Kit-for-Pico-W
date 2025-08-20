"""
LED Brightness Controller

Controls LED brightness using a potentiometer input.
Shows real-time values and provides smooth brightness control.
"""

import machine
import utime

# Pin definitions and constants
POTENTIOMETER_PIN = 28          # potentiometer connected to ADC pin 28
LED_PIN = 15                    # LED connected to pin 15
READING_DELAY = 100             # delay between readings in milliseconds

# ADC and PWM value ranges
MIN_ANALOG_VALUE = 0            # minimum analog reading
MAX_ANALOG_VALUE = 65535        # maximum analog reading (16-bit)
MIN_PWM_VALUE = 0               # minimum PWM output
MAX_PWM_VALUE = 65535           # maximum PWM output (16-bit)
PWM_FREQUENCY = 1000            # PWM frequency in Hz

# Change detection threshold
CHANGE_THRESHOLD = 1000         # minimum change to trigger display update

# Variables for brightness control
current_reading = 0             # current potentiometer reading
led_brightness = 0              # calculated LED brightness
last_reading = -1               # previous reading for change detection

# Initialize hardware
potentiometer = machine.ADC(POTENTIOMETER_PIN)
led = machine.PWM(machine.Pin(LED_PIN))
led.freq(PWM_FREQUENCY)

def map_value(value, from_min, from_max, to_min, to_max):
    """Map a value from one range to another"""
    return int((value - from_min) * (to_max - to_min) / (from_max - from_min) + to_min)

def show_control_info():
    """Display control information at startup"""
    print("=== LED Brightness Controller ===")
    print("Turn potentiometer to adjust brightness")
    print("Range: 0% to 100% brightness")
    print("================================")
    print()

def display_current_status():
    """Display current brightness status"""
    global current_reading, led_brightness
    
    # Calculate percentage for user-friendly display
    brightness_percent = map_value(led_brightness, MIN_PWM_VALUE, MAX_PWM_VALUE, 0, 100)
    
    print(f"Potentiometer: {current_reading} | LED Brightness: {led_brightness}/{MAX_PWM_VALUE} ({brightness_percent}%)")
    
    # Show visual brightness indicator
    print("Brightness: [", end="")
    bar_length = brightness_percent // 10  # scale to 0-10 for visual bar
    for i in range(10):
        if i < bar_length:
            print("█", end="")
        else:
            print("░", end="")
    print("]")
    print()

def update_brightness_control():
    """Read potentiometer and control LED brightness"""
    global current_reading, led_brightness, last_reading
    
    # Read current potentiometer value
    current_reading = potentiometer.read_u16()
    
    # Convert analog reading to PWM value for LED brightness
    led_brightness = map_value(current_reading, MIN_ANALOG_VALUE, MAX_ANALOG_VALUE,
                              MIN_PWM_VALUE, MAX_PWM_VALUE)
    
    # Apply brightness to LED
    led.duty_u16(led_brightness)
    
    # Only display info when value changes significantly (reduce serial spam)
    if abs(current_reading - last_reading) > CHANGE_THRESHOLD:
        display_current_status()
        last_reading = current_reading

def main():
    """Main function"""
    show_control_info()
    
    try:
        while True:
            # Read potentiometer and update LED
            update_brightness_control()
            
            # Wait before next reading
            utime.sleep_ms(READING_DELAY)
            
    except KeyboardInterrupt:
        print("\nShutting down...")
        # Turn off LED
        led.duty_u16(0)
        led.deinit()

if __name__ == "__main__":
    main()