"""
Buzzer Alert System

Creates different alert patterns using a buzzer.
Demonstrates various beeping patterns for different situations.
"""

import machine
import utime

# Pin and timing constants
BUZZER_PIN = 15                     # buzzer connected to pin 15
PATTERN_DELAY = 2000                # delay between different patterns
TOTAL_PATTERNS = 4                  # number of alert patterns

# Alert pattern settings
SHORT_BEEP = 200                    # short beep duration
LONG_BEEP = 600                     # long beep duration
QUICK_PAUSE = 100                   # short pause between beeps
MEDIUM_PAUSE = 400                  # medium pause between beeps

# Initialize buzzer
buzzer = machine.Pin(BUZZER_PIN, machine.Pin.OUT)

def beep(duration):
    """Generate a beep for specified duration"""
    buzzer.value(1)
    utime.sleep_ms(duration)
    buzzer.value(0)

def pause(duration):
    """Create a pause for specified duration"""
    utime.sleep_ms(duration)

def standard_alert():
    """Pattern 1: Standard alert - 4 short beeps"""
    for i in range(4):
        beep(SHORT_BEEP)
        pause(MEDIUM_PAUSE)

def sos_signal():
    """Pattern 2: SOS signal - 3 short, 3 long, 3 short"""
    # Three short beeps (S)
    for i in range(3):
        beep(SHORT_BEEP)
        pause(QUICK_PAUSE)
    
    pause(MEDIUM_PAUSE)
    
    # Three long beeps (O)
    for i in range(3):
        beep(LONG_BEEP)
        pause(QUICK_PAUSE)
    
    pause(MEDIUM_PAUSE)
    
    # Three short beeps (S)
    for i in range(3):
        beep(SHORT_BEEP)
        pause(QUICK_PAUSE)

def quick_warning():
    """Pattern 3: Quick warning - 6 rapid beeps"""
    for i in range(6):
        beep(SHORT_BEEP // 2)  # very short beeps
        pause(QUICK_PAUSE)

def alarm_sound():
    """Pattern 4: Alarm sound - alternating short and long beeps"""
    for i in range(3):
        # Short beep
        beep(SHORT_BEEP)
        pause(QUICK_PAUSE)
        
        # Long beep
        beep(LONG_BEEP)
        pause(QUICK_PAUSE)

def setup():
    """Initialize the buzzer alert system"""
    print("=== Buzzer Alert System ===")
    print("Demonstrating different alert patterns:")
    print("1. Standard Alert  2. SOS Signal")
    print("3. Quick Warning   4. Alarm Sound")
    print()

def main():
    """Main function"""
    setup()
    
    try:
        cycle_count = 0
        while True:
            cycle_count += 1
            print(f"--- Alert Cycle #{cycle_count} ---")
            
            # Pattern 1: Standard Alert (4 short beeps)
            print("Pattern 1: Standard Alert")
            standard_alert()
            pause(PATTERN_DELAY)
            
            # Pattern 2: SOS Signal (... --- ...)
            print("Pattern 2: SOS Emergency Signal")
            sos_signal()
            pause(PATTERN_DELAY)
            
            # Pattern 3: Quick Warning (rapid beeps)
            print("Pattern 3: Quick Warning")
            quick_warning()
            pause(PATTERN_DELAY)
            
            # Pattern 4: Alarm Sound (alternating tones)
            print("Pattern 4: Alarm Sound")
            alarm_sound()
            pause(PATTERN_DELAY)
            
            print("--- Cycle Complete ---")
            print()
            
    except KeyboardInterrupt:
        print("\nBuzzer alert system stopped.")
        print(f"Total cycles completed: {cycle_count}")
        
        # Turn off buzzer safely
        buzzer.value(0)
        print("Buzzer turned off.")

if __name__ == "__main__":
    main()