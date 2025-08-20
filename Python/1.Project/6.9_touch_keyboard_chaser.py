# 6.9_touch_keyboard_chaser.py
#
# This project uses an MPR121 capacitive touch sensor to trigger
# a "chaser" or "ripple" light effect on a WS2812 LED strip.
# Touching a key on the sensor creates a light pulse that
# spreads outwards from that point.
#
# Combines logic from:
# - 3.3_touch_keyboard.py (for MPR121 input)
# - 6.13_rfid_player.py (for WS2812 output)

from machine import Pin, I2C
from mpr121 import MPR121
from ws2812 import WS2812
import time

# --- Configuration ---
# MPR121 Touch Sensor Config (uses I2C bus 0)
I2C_SDA_PIN = 6
I2C_SCL_PIN = 7

# WS2812 LED Strip Config
WS2812_PIN = 16  # The GPIO pin connected to the data line of the LED strip
NUM_LEDS = 8    # The number of LEDs on the strip

# Animation Config
ANIMATION_SPEED_MS = 65  # Time in milliseconds between animation frames. Lower is faster.
ANIMATION_COLOR_RGB = (50, 150, 255) # A nice blue color (R, G, B) for the light effect.

class TouchChaser:
    """
    Manages the touch sensor and LED strip to create interactive light effects.
    """
    def __init__(self):
        """Initializes all hardware components and state variables."""
        print("Initializing Touch Keyboard Chaser...")

        # 1. Initialize I2C and MPR121 Touch Sensor
        self.i2c = I2C(1, sda=Pin(I2C_SDA_PIN), scl=Pin(I2C_SCL_PIN))
        self.mpr = MPR121(self.i2c)
        
        # 2. Initialize WS2812 LED Strip
        self.led_strip = WS2812(Pin(WS2812_PIN), NUM_LEDS)
        
        # 3. State tracking to detect new presses
        self.last_touched_keys = []
        
        # Convert RGB tuple to a single integer for the ws2812 library
        # The library typically expects colors in Green, Red, Blue (GRB) order.
        r, g, b = ANIMATION_COLOR_RGB
        self.animation_color_int = (g << 16) | (r << 8) | b
        
        self.clear_leds()
        print("Initialization complete. Ready for touch!")

    def clear_leds(self):
        """Turns all LEDs on the strip off."""
        for i in range(NUM_LEDS):
            self.led_strip[i] = 0
        self.led_strip.write()

    def play_ripple_animation(self, origin):
        """
        Plays the light animation, spreading outwards from a given origin point.
        
        Args:
            origin (int): The index of the LED where the animation should start.
        """
        print(f"Animation triggered from key {origin}")
        
        # Calculate how far the ripple needs to spread to cover the whole strip
        max_distance = max(origin, NUM_LEDS - 1 - origin)
        
        for distance in range(max_distance + 1):
            # In each frame, update the entire strip
            for i in range(NUM_LEDS):
                # Calculate this LED's distance from the origin
                dist_from_origin = abs(i - origin)
                
                # Light up the LED if it's at the current wavefront
                if dist_from_origin == distance:
                    self.led_strip[i] = self.animation_color_int
                else:
                    self.led_strip[i] = 0 # Turn all other LEDs off
            
            self.led_strip.write()
            time.sleep_ms(ANIMATION_SPEED_MS)
        
        # Hold the final frame briefly before clearing the strip
        time.sleep_ms(200)
        self.clear_leds()

    def run(self):
        """The main loop that continuously checks for touches and runs animations."""
        while True:
            current_touched_keys = self.mpr.get_all_states()
            
            # A "new touch" is when the current state is not empty and is different from the last state.
            # This triggers the animation only on the initial press, not while holding.
            is_new_touch = bool(current_touched_keys) and (current_touched_keys != self.last_touched_keys)
            
            if is_new_touch:
                # We use the first key in the list if multiple are touched simultaneously.
                origin_key = current_touched_keys[0]
                
                # Map the 12 keys of the MPR121 to the 8 LEDs on the strip.
                # We only care about the first 8 keys (0-7).
                if 0 <= origin_key < NUM_LEDS:
                    self.play_ripple_animation(origin_key)
                else:
                    print(f"Info: Touched key {origin_key} is outside the LED strip range (0-{NUM_LEDS-1}).")

            # Update the state for the next cycle
            self.last_touched_keys = current_touched_keys
            
            # A small delay to keep the system responsive without overwhelming the CPU
            time.sleep_ms(20)

def main():
    """The main entry point of the program."""
    try:
        chaser_app = TouchChaser()
        chaser_app.run()
    except KeyboardInterrupt:
        print("\nProgram stopped by user.")
        # Create a temporary object to turn off LEDs on exit
        # This ensures the strip is dark even if the program is stopped mid-animation.
        try:
            temp_led_strip = WS2812(Pin(WS2812_PIN), NUM_LEDS)
            for i in range(NUM_LEDS):
                temp_led_strip[i] = 0
            temp_led_strip.write()
        except Exception as e:
            print(f"Could not turn off LEDs on exit: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
    finally:
        print("Shutting down.")

if __name__ == "__main__":
    main()
