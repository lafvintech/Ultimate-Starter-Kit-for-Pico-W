"""
Magnetic Presence Detector

Detects when a magnet is near using a reed switch.
Provides user-friendly feedback and tracks detection events.

Note: Reed switches detect presence/absence, not magnetic strength.
"""

import machine
import utime

# Pin definition for the reed switch
REED_SWITCH = 14                    # reed switch connected to pin 14

# Timing constants
SCAN_DELAY = 100                    # delay between scans in milliseconds
PRESENCE_CHECK_INTERVAL = 5000      # when to start showing duration (ms)
DURATION_UPDATE_INTERVAL = 3000     # how often to update duration display (ms)
DURATION_UPDATE_TOLERANCE = 100     # tolerance for duration update timing (ms)

# Variables to track magnetic presence
magnet_present = False              # current state (True = magnet detected)
last_magnet_state = False           # previous state for change detection
detection_time = 0                  # when magnet was first detected
total_detections = 0                # count of total detections

# Initialize reed switch
reed_switch = machine.Pin(REED_SWITCH, machine.Pin.IN)

def initialize_detector():
    """Display welcome message and initialize system"""
    print("=== Magnetic Presence Detector ===")
    print("Bring a magnet close to the sensor")
    print("System ready for detection...")
    print("==================================")
    print()

def trigger_detection_alert():
    """Announce when a magnet is detected"""
    global total_detections, detection_time
    
    print("*** MAGNET DETECTED! ***")
    
    # Show detection details
    print(f"Detection #{total_detections}")
    print(f"Time: {detection_time} ms")
    print("Status: ACTIVE")
    print()

def scan_magnetic_field():
    """Check for magnetic field presence and detect changes"""
    global magnet_present, last_magnet_state, detection_time, total_detections
    
    # Read current reed switch state
    magnet_present = bool(reed_switch.value())
    
    # Check if magnet was just detected (state change from absent to present)
    if magnet_present and not last_magnet_state:
        # Record detection time and increment counter
        detection_time = utime.ticks_ms()
        total_detections += 1
        
        # Announce detection
        trigger_detection_alert()
    
    # Check if magnet was removed (state change from present to absent)
    if not magnet_present and last_magnet_state:
        print("--- Magnet removed ---")
        print("Field cleared")
        print()
    
    # Remember current state for next comparison
    last_magnet_state = magnet_present

def update_presence_monitor():
    """Monitor continuous magnetic presence"""
    global magnet_present, detection_time
    
    # If magnet has been present for more than 5 seconds, show duration
    if magnet_present and detection_time > 0:
        current_time = utime.ticks_ms()
        duration_ms = utime.ticks_diff(current_time, detection_time)
        
        if duration_ms > PRESENCE_CHECK_INTERVAL:
            # Only show message every 3 seconds to avoid spam
            if (duration_ms % DURATION_UPDATE_INTERVAL) < DURATION_UPDATE_TOLERANCE:
                print(">> Magnet still present <<")
                print(f"Duration: {duration_ms // 1000} seconds")
                print()

def main():
    """Main function"""
    initialize_detector()
    
    try:
        while True:
            # Check for magnetic presence
            scan_magnetic_field()
            
            # Update continuous presence monitoring
            update_presence_monitor()
            
            # Small delay for stability
            utime.sleep_ms(SCAN_DELAY)
            
    except KeyboardInterrupt:
        print("\nMagnetic detection system stopped.")
        print(f"Total detections: {total_detections}")
        if magnet_present:
            current_time = utime.ticks_ms()
            final_duration = utime.ticks_diff(current_time, detection_time) // 1000
            print(f"Final detection duration: {final_duration} seconds")

if __name__ == "__main__":
    main()