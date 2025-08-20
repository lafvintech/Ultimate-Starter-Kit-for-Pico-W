# 6.10_reversing_alarm.py
# A professional, feature-rich reversing alarm system for MicroPython,
# inspired by a well-structured Raspberry Pi example.
#
# This system measures distance using an HC-SR04 ultrasonic sensor and provides
# distinct visual and audio alerts based on proximity zones.

import machine
import time
import sys

# --- Configuration ---
# Hardware Pins
TRIG_PIN = 17       # Ultrasonic sensor Trigger pin
ECHO_PIN = 16       # Ultrasonic sensor Echo pin
BUZZER_PIN = 15     # Buzzer pin
LED_PIN = 14        # LED pin

# Proximity Zones (in cm)
DANGER_ZONE_CM = 20   # Less than this is DANGER
WARNING_ZONE_CM = 50  # Less than this is WARNING
# Anything above WARNING_ZONE_CM is considered SAFE.

class ReversingAlarmSystem:
    """
    Manages all functionality for the reversing alarm system.
    """
    def __init__(self):
        """Initializes all hardware components."""
        print("🔧 Initializing Reversing Alarm System...")
        
        self.trig = machine.Pin(TRIG_PIN, machine.Pin.OUT)
        self.echo = machine.Pin(ECHO_PIN, machine.Pin.IN)
        self.buzzer = machine.Pin(BUZZER_PIN, machine.Pin.OUT)
        self.led = machine.Pin(LED_PIN, machine.Pin.OUT)
        
        self.cleanup() # Ensure all outputs are off initially
        print("✅ System Ready. Press Ctrl+C to exit.")

    def measure_distance(self):
        """
        Measures distance using the HC-SR04 sensor.
        Returns the distance in centimeters, or -1 on timeout.
        """
        # Send a 10µs trigger pulse
        self.trig.low()
        time.sleep_us(2)
        self.trig.high()
        time.sleep_us(10)
        self.trig.low()

        # Wait for the echo pulse to start, with a timeout
        # This prevents the program from getting stuck if the sensor is disconnected.
        timeout_us = 30000 # 30ms, corresponds to ~5 meters, well beyond our needs.
        start_time = time.ticks_us()
        while not self.echo.value():
            if time.ticks_diff(time.ticks_us(), start_time) > timeout_us:
                return -1 # Timeout error

        pulse_start = time.ticks_us()

        # Wait for the echo pulse to end, with a timeout
        while self.echo.value():
            if time.ticks_diff(time.ticks_us(), pulse_start) > timeout_us:
                return -1 # Timeout error

        pulse_end = time.ticks_us()

        # Calculate distance: (pulse_duration * speed_of_sound) / 2
        # Speed of sound is ~343 m/s or 34,300 cm/s or 0.0343 cm/µs
        pulse_duration = time.ticks_diff(pulse_end, pulse_start)
        distance_cm = (pulse_duration * 0.0343) / 2
        
        return distance_cm

    def play_alert(self, distance):
        """
        Plays a specific alert pattern on the LED and buzzer based on the distance.
        """
        if distance < 0:
            print("Sensor timeout. Check wiring.")
            time.sleep(0.5)
            return

        if distance <= DANGER_ZONE_CM:
            # DANGER ZONE: Fast, continuous beeps
            print(f"🚨 DANGER!  Distance: {distance:.1f} cm")
            self.led.high()
            self.buzzer.high()
            time.sleep(0.07)
            self.led.low()
            self.buzzer.low()
            time.sleep(0.07)
        
        elif distance <= WARNING_ZONE_CM:
            # WARNING ZONE: Slower, intermittent beeps
            print(f"⚠️ WARNING! Distance: {distance:.1f} cm")
            self.led.high()
            self.buzzer.high()
            time.sleep(0.1)
            self.led.low()
            self.buzzer.low()
            time.sleep(0.3) # Longer pause
            
        else:
            # SAFE ZONE: No sound, solid LED for feedback
            print(f"✅ SAFE.    Distance: {distance:.1f} cm")
            self.led.low() # Or you could turn it on to show it's "active"
            self.buzzer.low()
            time.sleep(0.5) # Longer delay in the safe zone

    def cleanup(self):
        """Turns off all hardware outputs to ensure a safe state."""
        self.buzzer.low()
        self.led.low()

    def run(self):
        """The main interactive loop for the alarm system."""
        print("\n" + "="*40)
        print("🎯 Smart Reversing Alarm System is Active")
        print(f"   - 🚨 Danger:  < {DANGER_ZONE_CM} cm")
        print(f"   - ⚠️ Warning: < {WARNING_ZONE_CM} cm")
        print("="*40 + "\n")

        while True:
            distance = self.measure_distance()
            self.play_alert(distance)
            
def main():
    """Main function to start the application."""
    alarm_system = ReversingAlarmSystem()
    
    try:
        alarm_system.run()
    except KeyboardInterrupt:
        print("\n🛑 Program interrupted by user.")
    finally:
        alarm_system.cleanup()
        print("🧹 System shut down. All outputs are off.")

if __name__ == '__main__':
    main()
