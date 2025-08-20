"""
Transistor Switch Control

Uses a button to control a transistor switch that can
drive higher current devices like motors or lights.
"""

import machine
import utime

# Pin definitions
BUTTON_PIN = 14                     # button input pin
TRANSISTOR_PIN = 15                 # transistor control pin
CHECK_DELAY = 50                    # button check interval in milliseconds

# Variables for button state tracking
button_pressed = False
last_button_state = False
device_on = False
press_count = 0

# Initialize pins
button = machine.Pin(BUTTON_PIN, machine.Pin.IN)
transistor = machine.Pin(TRANSISTOR_PIN, machine.Pin.OUT)

def setup():
    """Initialize the system"""
    global device_on
    
    print("=== Transistor Switch Control ===")
    print("Press button to toggle device ON/OFF")
    print("Transistor acts as electronic switch")
    print()
    
    # Ensure device starts OFF
    transistor.value(0)
    device_on = False
    print("Device: OFF (Ready)")
    print()

def handle_button_control():
    """Handle button press and transistor control"""
    global button_pressed, last_button_state, device_on, press_count
    
    # Read current button state
    button_pressed = bool(button.value())
    
    # Detect button press (transition from LOW to HIGH)
    if button_pressed and not last_button_state:
        # Toggle device state
        device_on = not device_on
        press_count += 1
        
        # Control transistor switch
        transistor.value(1 if device_on else 0)
        
        # Display status
        print(f"Button pressed (#{press_count}) - Device: {'ON' if device_on else 'OFF'}")
        
        if device_on:
            print("Transistor conducting - High current device active")
        else:
            print("Transistor off - High current device inactive")
        print()
    
    # Update last button state for next comparison
    last_button_state = button_pressed

def main():
    """Main function"""
    setup()
    
    try:
        while True:
            # Check button and control transistor
            handle_button_control()
            
            # Small delay for stable operation
            utime.sleep_ms(CHECK_DELAY)
            
    except KeyboardInterrupt:
        print("\nTransistor control stopped.")
        print(f"Total button presses: {press_count}")
        
        # Turn off device safely
        transistor.value(0)
        print("Device turned OFF - System safe.")

if __name__ == "__main__":
    main()