import machine
import time

# Hardware Pin Constants
BUZZER_PIN = 15
LED_PIN = 16
SWITCH_PIN = 17

# PWM and Frequency Constants
LED_PWM_FREQUENCY = 1000
BUZZER_DUTY_CYCLE = 30000

# Alarm Effect Constants  
EFFECT_STEPS = 100
EFFECT_INCREMENT = 2
EFFECT_DELAY_MS = 10

# Sound Frequency Range
MIN_FREQUENCY = 130
MAX_FREQUENCY = 800

# LED Brightness Range
MIN_BRIGHTNESS = 0
MAX_BRIGHTNESS = 65535

# Alarm Modes
MODE_SWEEP = 0
MODE_PULSE = 1
MODE_RAPID = 2

# Initialize hardware components
buzzer = machine.PWM(machine.Pin(BUZZER_PIN))
led = machine.PWM(machine.Pin(LED_PIN))
led.freq(LED_PWM_FREQUENCY)
switch = machine.Pin(SWITCH_PIN, machine.Pin.IN)

# Global variables
alarm_active = False
alarm_mode = MODE_SWEEP

def stop_buzzer(pwm_pin):
    """Turn off the buzzer by setting duty cycle to zero"""
    pwm_pin.duty_u16(0)

def play_tone(pwm_pin, frequency):
    """Play a tone at specified frequency on the buzzer"""
    pwm_pin.freq(frequency)
    pwm_pin.duty_u16(BUZZER_DUTY_CYCLE)

def map_value(x, in_min, in_max, out_min, out_max):
    """Map a value from one range to another"""
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def sweep_alarm_effect():
    """Create a sweeping alarm effect with gradual frequency and brightness change"""
    for step in range(0, EFFECT_STEPS, EFFECT_INCREMENT):
        if not alarm_active:
            break
        
        # Calculate LED brightness and buzzer frequency
        brightness = int(map_value(step, 0, EFFECT_STEPS, MIN_BRIGHTNESS, MAX_BRIGHTNESS))
        frequency = int(map_value(step, 0, EFFECT_STEPS, MIN_FREQUENCY, MAX_FREQUENCY))
        
        # Apply effects
        led.duty_u16(brightness)
        play_tone(buzzer, frequency)
        time.sleep_ms(EFFECT_DELAY_MS)

def pulse_alarm_effect():
    """Create a pulsing alarm effect with on/off cycles"""
    # High intensity pulse
    led.duty_u16(MAX_BRIGHTNESS)
    play_tone(buzzer, MAX_FREQUENCY)
    time.sleep_ms(200)
    
    # Off period
    led.duty_u16(MIN_BRIGHTNESS)
    stop_buzzer(buzzer)
    time.sleep_ms(100)

def rapid_alarm_effect():
    """Create a rapid flashing alarm effect"""
    # Quick flash sequence
    for _ in range(5):
        if not alarm_active:
            break
        led.duty_u16(MAX_BRIGHTNESS)
        play_tone(buzzer, MIN_FREQUENCY + MAX_FREQUENCY // 2)
        time.sleep_ms(50)
        
        led.duty_u16(MIN_BRIGHTNESS)
        stop_buzzer(buzzer)
        time.sleep_ms(50)

def run_alarm_effect():
    """Execute the appropriate alarm effect based on current mode"""
    if alarm_mode == MODE_SWEEP:
        sweep_alarm_effect()
    elif alarm_mode == MODE_PULSE:
        pulse_alarm_effect()
    elif alarm_mode == MODE_RAPID:
        rapid_alarm_effect()

def turn_off_alarm():
    """Turn off both buzzer and LED"""
    stop_buzzer(buzzer)
    led.duty_u16(MIN_BRIGHTNESS)

def display_mode_selection():
    """Display mode selection menu"""
    print("\n" + "="*50)
    print("        ALARM SIREN LAMP - MODE SELECTION")
    print("="*50)
    print("Available alarm modes:")
    print("  0 - Sweep Mode   (Gradual frequency sweep)")
    print("  1 - Pulse Mode   (On/off pulsing)")
    print("  2 - Rapid Mode   (Fast flashing)")
    print("-"*50)

def select_alarm_mode():
    """Allow user to select alarm mode at startup"""
    global alarm_mode
    
    mode_names = ["Sweep", "Pulse", "Rapid"]
    
    while True:
        display_mode_selection()
        try:
            user_input = input("Please select mode (0-2): ").strip()
            mode = int(user_input)
            
            if 0 <= mode <= 2:
                alarm_mode = mode
                print(f"\n✓ Mode selected: {mode} ({mode_names[mode]})")
                
                # Mode confirmation beep
                play_tone(buzzer, 500 + mode * 200)
                time.sleep_ms(200)
                stop_buzzer(buzzer)
                
                print(f"Alarm system is ready in {mode_names[mode]} mode!")
                print("Toggle the switch to activate the alarm.")
                print("To change mode, restart the program.\n")
                return
            else:
                print("❌ Invalid mode! Please enter 0, 1, or 2\n")
                
        except ValueError:
            print("❌ Invalid input! Please enter a number (0-2)\n")
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user. Goodbye!")
            turn_off_alarm()  # Ensure everything is turned off
            raise SystemExit

def switch_interrupt_handler(pin):
    """Handle switch state changes for alarm on/off control"""
    global alarm_active
    
    alarm_active = pin.value()
    mode_names = ["Sweep", "Pulse", "Rapid"]
    
    if alarm_active:
        print(f"🚨 Alarm activated - Mode: {mode_names[alarm_mode]}")
        
        # Startup confirmation beep
        play_tone(buzzer, 1000)
        led.duty_u16(MAX_BRIGHTNESS // 2)
        time.sleep_ms(100)
        turn_off_alarm()
        time.sleep_ms(50)
    else:
        print("✅ Alarm deactivated")
        turn_off_alarm()

# Main program starts here
def main():
    """Main program function"""
    print("\n🚨 ALARM SIREN LAMP SYSTEM 🚨")
    print("Copyright 2024 - IoT Alarm Project")
    
    # Let user select the alarm mode
    select_alarm_mode()
    
    # Configure switch interrupt for both rising and falling edges
    switch.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, 
              handler=switch_interrupt_handler)
    
    print("🔄 System running... (Press Ctrl+C to exit)")
    
    try:
        # Main program loop
        while True:
            if alarm_active:
                run_alarm_effect()
            else:
                turn_off_alarm()
                time.sleep_ms(50)  # Small delay when inactive
                
    except KeyboardInterrupt:
        print("\n\n👋 Program stopped by user")
        turn_off_alarm()
        print("All devices turned off. Goodbye!")

# Run the main program
if __name__ == "__main__":
    main()