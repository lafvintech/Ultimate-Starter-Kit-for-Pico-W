"""
74HC595 Smooth Flowing LED Project

Creates a smooth flowing LED effect using a 74HC595 shift register.
LEDs progressively light up and then smoothly flow back, creating
a continuous mesmerizing water-like animation.

Hardware: 74HC595 shift register + 8 LEDs with current limiting resistors
"""

import machine
import time

# 74HC595 Pin Configuration Constants
DATA_PIN = 0        # DS (Serial Data Input) - pin 14 of 74HC595
LATCH_PIN = 1       # ST_CP (Storage Register Clock) - pin 12 of 74HC595
CLOCK_PIN = 2       # SH_CP (Shift Register Clock) - pin 11 of 74HC595

# Animation Timing Constants
FLOW_DELAY_MS = 150  # Delay between flow steps for smooth animation

class HC595FlowingLED:
    """74HC595 Smooth Flowing LED Controller"""
    
    def __init__(self):
        """Initialize 74HC595 control pins"""
        self.data_pin = machine.Pin(DATA_PIN, machine.Pin.OUT)
        self.latch_pin = machine.Pin(LATCH_PIN, machine.Pin.OUT)
        self.clock_pin = machine.Pin(CLOCK_PIN, machine.Pin.OUT)
        
        # Smooth Flowing LED Patterns
        self.flow_patterns = [
            0b00000000,  # All off (start)
            0b00000001,  # 1 LED
            0b00000011,  # 2 LEDs
            0b00000111,  # 3 LEDs
            0b00001111,  # 4 LEDs
            0b00011111,  # 5 LEDs
            0b00111111,  # 6 LEDs
            0b01111111,  # 7 LEDs
            0b11111111,  # All on (peak)
            0b11111110,  # Flow back: 7 LEDs
            0b11111100,  # 6 LEDs
            0b11111000,  # 5 LEDs
            0b11110000,  # 4 LEDs
            0b11100000,  # 3 LEDs
            0b11000000,  # 2 LEDs
            0b10000000,  # 1 LED
            0b00000000   # All off (end cycle)
        ]
        
        # Clear all LEDs initially
        self.update_shift_register(0b00000000)
        print("74HC595 Smooth Flowing LED initialized")
    
    def update_shift_register(self, pattern):
        """
        Update Shift Register
        Sends data to 74HC595 and latches the output.
        """
        self.latch_pin.low()                           # Prepare for data
        self.shift_out_msb_first(pattern)              # Send 8 bits
        self.latch_pin.high()                          # Latch data to outputs
    
    def shift_out_msb_first(self, data):
        """
        Shift out data MSB first (Most Significant Bit first)
        Equivalent to Arduino's shiftOut() function
        """
        for bit in range(7, -1, -1):  # Start from bit 7 down to bit 0
            self.clock_pin.low()
            time.sleep_ms(1)
            
            # Extract the bit value
            bit_value = (data >> bit) & 1
            self.data_pin.value(bit_value)
            time.sleep_ms(1)
            
            self.clock_pin.high()
            time.sleep_ms(1)
    
    def run_smooth_flowing_animation(self):
        """
        Run Smooth Flowing Animation
        Creates a mesmerizing water-like flow effect that builds up
        all LEDs then smoothly flows back to create continuous motion.
        """
        for i, pattern in enumerate(self.flow_patterns):
            self.update_shift_register(pattern)
            print(f"Step {i:2d}: {pattern:08b}")
            time.sleep_ms(FLOW_DELAY_MS)
    
    def run_continuous_animation(self):
        """Run continuous smooth flowing animation"""
        print("Starting smooth flowing LED animation...")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                self.run_smooth_flowing_animation()
        except KeyboardInterrupt:
            print("\nAnimation stopped")
            self.update_shift_register(0b00000000)  # Clear all LEDs
    
    def test_all_leds(self):
        """Test all LEDs individually"""
        print("Testing all LEDs individually...")
        
        for i in range(8):
            pattern = 1 << i  # Light up LED i
            self.update_shift_register(pattern)
            print(f"LED {i}: {pattern:08b}")
            time.sleep_ms(300)
        
        # Turn off all LEDs
        self.update_shift_register(0b00000000)
        print("LED test complete")
    
    def custom_pattern(self, pattern):
        """Display a custom pattern"""
        self.update_shift_register(pattern)
        print(f"Custom pattern: {pattern:08b}")

# Create and run the flowing LED controller
if __name__ == "__main__":
    try:
        led_controller = HC595FlowingLED()
        
        # Optional: Test all LEDs first
        # led_controller.test_all_leds()
        # time.sleep_ms(1000)
        
        # Run continuous smooth flowing animation
        led_controller.run_continuous_animation()
        
    except Exception as e:
        print(f"Error: {e}")