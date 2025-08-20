"""
Tilt Switch Monitor

Reads a tilt switch and reports when the orientation changes.
Shows different messages for tilt and level positions.
"""

import machine
import utime

# Pin definition - connect tilt switch to this pin
TILT_PIN = 14               # tilt switch connected to pin 14

# Timing constants
MONITOR_DELAY = 100         # delay between checks in milliseconds

# Variables to track switch state
current_state = 0           # current reading from tilt switch
last_state = 0              # previous reading to detect changes
show_welcome = True         # flag to show welcome message once

# Initialize tilt switch
tilt_switch = machine.Pin(TILT_PIN, machine.Pin.IN)

def show_welcome_message():
    """Display welcome message with initial state"""
    global last_state, show_welcome
    
    print("=== Tilt Switch Monitor ===")
    
    # Determine initial position
    initial_position = "TILTED" if last_state == 0 else "LEVEL"
    print(f"Current position: {initial_position}")
    print("Move the sensor to see changes...")
    print()
    
    show_welcome = False

def monitor_tilt_switch():
    """Read tilt switch and detect state changes"""
    global current_state, last_state
    
    # Read current tilt switch state
    current_state = tilt_switch.value()
    
    # Check if state changed (only act on changes, not continuous reading)
    if current_state != last_state:
        # Print timestamp for the change
        timestamp = utime.ticks_ms()
        print(f"[{timestamp}ms] ", end="")
        
        # Check new position and print appropriate message
        if current_state == 0:  # LOW state (tilted)
            print(">>> SENSOR TILTED <<<")
            print("Position changed to: TILTED")
        else:  # HIGH state (level)
            print("--- Sensor Level ---")
            print("Position changed to: LEVEL")
        
        print()  # blank line for readability
        
        # Remember this state for next comparison
        last_state = current_state

def initialize_system():
    """Initialize the tilt monitoring system"""
    global last_state
    
    # Read initial state
    last_state = tilt_switch.value()

def main():
    """Main function"""
    global show_welcome
    
    # Initialize system
    initialize_system()
    
    try:
        while True:
            # Show welcome message once at start
            if show_welcome:
                show_welcome_message()
            
            # Monitor tilt switch for changes
            monitor_tilt_switch()
            
            # Small delay for stability
            utime.sleep_ms(MONITOR_DELAY)
            
    except KeyboardInterrupt:
        print("\nTilt switch monitoring stopped.")
        
        # Show final state
        final_position = "TILTED" if current_state == 0 else "LEVEL"
        print(f"Final position: {final_position}")

if __name__ == "__main__":
    main()
