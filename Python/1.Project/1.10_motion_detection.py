"""
Motion Detection Alert System

Uses a PIR sensor to detect motion and provides 
alert messages with detection counting.
"""

import machine
import utime

# Pin definition and constants
PIR_SENSOR_PIN = 14             # PIR sensor connected to pin 14
DETECTION_DELAY = 200           # delay between readings in milliseconds

# Variables for motion tracking
motion_detected = False         # current motion state
last_motion_state = False       # previous state for change detection
detection_count = 0             # total number of detections
last_detection_time = 0         # timestamp of last detection

# Initialize PIR sensor
pir_sensor = machine.Pin(PIR_SENSOR_PIN, machine.Pin.IN)

def show_startup_message():
    """Display startup information"""
    print("=== Motion Detection System ===")
    print("PIR sensor monitoring active")
    print("Waiting for motion...")
    print("==============================")
    print()

def trigger_motion_alert():
    """Handle motion detection alert"""
    global detection_count, last_detection_time
    
    print(">>> MOTION DETECTED! <<<")
    print("Alert: Movement in monitored area")
    
    # Show detection statistics
    print(f"Detection #{detection_count}")
    print(f"Time: {last_detection_time} ms")
    print("Status: ACTIVE")
    print()

def check_motion_sensor():
    """Monitor PIR sensor and detect motion changes"""
    global motion_detected, last_motion_state, detection_count, last_detection_time
    
    # Read current PIR sensor state
    motion_detected = pir_sensor.value()
    
    # Check if motion was just detected (state change from no motion to motion)
    if motion_detected and not last_motion_state:
        # Record detection time and increment counter
        last_detection_time = utime.ticks_ms()
        detection_count += 1
        
        # Trigger motion alert
        trigger_motion_alert()
    
    # Check if motion stopped (state change from motion to no motion)
    if not motion_detected and last_motion_state:
        print("Motion stopped - area clear")
        print()
    
    # Update last state for next comparison
    last_motion_state = motion_detected

def main():
    """Main function"""
    show_startup_message()
    
    try:
        while True:
            # Check for motion detection
            check_motion_sensor()
            
            # Wait before next reading
            utime.sleep_ms(DETECTION_DELAY)
            
    except KeyboardInterrupt:
        print("\nMotion detection system stopped.")
        print(f"Total detections: {detection_count}")

if __name__ == "__main__":
    main()