"""
Automatic Night Light

Uses a photoresistor to control LED brightness automatically.
Bright environment = dim LED, dark environment = bright LED.
"""

import machine
import utime

# Pin connections
LIGHT_SENSOR_PIN = 28           # photoresistor on ADC pin 28
LED_PIN = 15                    # LED on digital pin 15

# Settings
UPDATE_DELAY = 200              # how often to check sensor (milliseconds)

# ADC and PWM constants
ADC_MAX_VALUE = 65535           # 16-bit ADC maximum value
PWM_MAX_VALUE = 65535           # 16-bit PWM maximum value
PWM_FREQUENCY = 1000            # PWM frequency in Hz

# Initialize hardware
photoresistor = machine.ADC(LIGHT_SENSOR_PIN)
led = machine.PWM(machine.Pin(LED_PIN))
led.freq(PWM_FREQUENCY)

def map_value(value, from_min, from_max, to_min, to_max):
    """Map a value from one range to another"""
    return int((value - from_min) * (to_max - to_min) / (from_max - from_min) + to_min)

def read_and_control_light():
    """Read light sensor and control LED brightness"""
    # Read light sensor (0-65535)
    light_reading = photoresistor.read_u16()
    
    # Convert to LED brightness (0-65535)
    # Note: our sensor gives HIGH values in dark, LOW values in bright light
    led_brightness = map_value(light_reading, 0, ADC_MAX_VALUE, 0, PWM_MAX_VALUE)
    
    # Set LED brightness using PWM
    led.duty_u16(led_brightness)
    
    # Show current values
    print(f"Light sensor: {light_reading} -> LED brightness: {led_brightness}/{PWM_MAX_VALUE}", end="")
    
    # Show simple status
    if light_reading > 45000:  # Dark environment threshold (16-bit ADC)
        print(" (Dark - LED bright)")
    elif light_reading > 26000:  # Medium light threshold (16-bit ADC)
        print(" (Medium - LED medium)")
    else:
        print(" (Bright - LED dim)")

def main():
    """Main function"""
    print("Automatic Night Light Started!")
    print("Cover sensor = LED gets brighter")
    print("Expose sensor to light = LED gets dimmer")
    print()
    
    try:
        while True:
            # Read sensor and control LED
            read_and_control_light()
            
            # Wait before next reading
            utime.sleep_ms(UPDATE_DELAY)
            
    except KeyboardInterrupt:
        print("\nShutting down...")
        # Turn off LED
        led.duty_u16(0)
        led.deinit()

if __name__ == "__main__":
    main()