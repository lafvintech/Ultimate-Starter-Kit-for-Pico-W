"""
Chaotic Random LED Strip

Each LED changes to random colors at random intervals,
creating a completely unpredictable light display.
"""

import machine
import utime
import urandom
from ws2812 import WS2812

# Hardware configuration
PIXEL_PIN = 0                       # NeoPixel strip pin
PIXEL_COUNT = 8                     # Number of LEDs in strip

# Random timing ranges (milliseconds)
MIN_CHANGE_TIME = 500               # Minimum time before LED can change color
MAX_CHANGE_TIME = 3000              # Maximum time before LED can change color

# LED data structure to track each LED independently
class LEDData:
    def __init__(self):
        self.next_change_time = 0   # When this LED should change color next
        self.current_color = [0, 0, 0]  # Current color of this LED [R, G, B]

# Array to store data for each LED
leds = [LEDData() for _ in range(PIXEL_COUNT)]

# Initialize WS2812 strip
strip = WS2812(machine.Pin(PIXEL_PIN), PIXEL_COUNT)

def generate_random_color():
    """Generate a completely random RGB color"""
    # Generate random RGB values (0-255 each)
    red = urandom.randint(0, 255)
    green = urandom.randint(0, 255)
    blue = urandom.randint(0, 255)
    
    # Occasionally generate pure colors for variety
    if urandom.randint(0, 9) == 0:  # 10% chance
        pure_colors = [
            [255, 0, 0],     # Pure red
            [0, 255, 0],     # Pure green
            [0, 0, 255],     # Pure blue
            [255, 255, 0],   # Yellow
            [255, 0, 255],   # Magenta
            [0, 255, 255]    # Cyan
        ]
        return pure_colors[urandom.randint(0, 5)]
    
    return [red, green, blue]

def print_color_info(color):
    """Print color information in readable format"""
    print(f"RGB({color[0]},{color[1]},{color[2]})", end="")

def setup():
    """Initialize the chaotic LED system"""
    print("=== Chaotic Random LED Strip ===")
    print("Each LED changes color independently at random intervals")
    print("Creating completely unpredictable light patterns")
    print()
    
    # Initialize each LED with random color and random next change time
    current_time = utime.ticks_ms()
    
    for i in range(PIXEL_COUNT):
        leds[i].current_color = generate_random_color()
        leds[i].next_change_time = current_time + urandom.randint(MIN_CHANGE_TIME, MAX_CHANGE_TIME)
        strip[i] = leds[i].current_color
        
        # Show initial color info
        print(f"LED {i} initialized: ", end="")
        print_color_info(leds[i].current_color)
        next_change_seconds = (leds[i].next_change_time - current_time) / 1000.0
        print(f", next change in {next_change_seconds:.1f} seconds")
    
    # Display initial colors
    strip.write()
    print()
    print("Starting chaotic color changes...")
    print()

def main():
    """Main function"""
    setup()
    
    try:
        while True:
            current_time = utime.ticks_ms()
            any_led_changed = False
            
            # Check each LED independently
            for i in range(PIXEL_COUNT):
                # Check if this LED should change color now
                if utime.ticks_diff(current_time, leds[i].next_change_time) >= 0:
                    # Generate new random color
                    leds[i].current_color = generate_random_color()
                    
                    # Set new random time for next change
                    leds[i].next_change_time = current_time + urandom.randint(MIN_CHANGE_TIME, MAX_CHANGE_TIME)
                    
                    # Update the LED
                    strip[i] = leds[i].current_color
                    
                    # Log the change
                    print(f"LED {i} changed to ", end="")
                    print_color_info(leds[i].current_color)
                    next_change_seconds = urandom.randint(MIN_CHANGE_TIME, MAX_CHANGE_TIME) / 1000.0
                    print(f", next change in {next_change_seconds:.1f} seconds")
                    
                    any_led_changed = True
            
            # Update strip only if any LED changed (efficiency)
            if any_led_changed:
                strip.write()
            
            # Small delay to prevent excessive CPU usage
            utime.sleep_ms(50)
            
    except KeyboardInterrupt:
        print("\nChaotic LED display stopped.")
        
        # Turn off all LEDs safely
        for i in range(PIXEL_COUNT):
            strip[i] = [0, 0, 0]
        strip.write()
        print("All LEDs turned off.")

if __name__ == "__main__":
    main()