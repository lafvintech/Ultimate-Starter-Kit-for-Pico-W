"""
DC Motor and Fan Control Project

This project demonstrates bidirectional control of a DC motor or fan
using digital pins with TA6586 motor driver IC. The motor alternates 
between clockwise rotation, stop, counterclockwise rotation, and stop 
in a continuous cycle.

Hardware Requirements:
- Raspberry Pi Pico or compatible board
- DC motor or fan
- TA6586 motor driver IC (dual H-bridge)
- Appropriate power supply for motor
"""

# Import required libraries
import machine  # For hardware control (Pin)
import utime    # For time delays

# Hardware Configuration Constants
MOTOR_PIN_A = 14            # TA6586 IN1 pin (motor direction control)
MOTOR_PIN_B = 15            # TA6586 IN2 pin (motor direction control)

# Timing Constants
ROTATION_DURATION_MS = 1000 # How long motor runs in each direction (milliseconds)
STOP_DURATION_MS = 1000     # How long motor stops between direction changes (milliseconds)

# Initialize motor control pins
motor_pin_a = machine.Pin(MOTOR_PIN_A, machine.Pin.OUT)
motor_pin_b = machine.Pin(MOTOR_PIN_B, machine.Pin.OUT)

def rotate_clockwise():
    """
    Rotate Motor Clockwise
    
    Sets the TA6586 motor driver pins to rotate the motor in clockwise direction.
    IN1 is set HIGH and IN2 is set LOW to create the forward direction signal.
    """
    print("Motor rotating clockwise...")
    motor_pin_a.on()   # Set TA6586 IN1 HIGH
    motor_pin_b.off()  # Set TA6586 IN2 LOW

def rotate_counterclockwise():
    """
    Rotate Motor Counterclockwise
    
    Sets the TA6586 motor driver pins to rotate the motor in counterclockwise direction.
    IN1 is set LOW and IN2 is set HIGH to create the reverse direction signal.
    """
    print("Motor rotating counterclockwise...")
    motor_pin_a.off()  # Set TA6586 IN1 LOW
    motor_pin_b.on()   # Set TA6586 IN2 HIGH

def stop_motor():
    """
    Stop Motor
    
    Stops the motor by setting both TA6586 control pins to LOW.
    This puts the motor driver in brake/stop mode, causing the motor to stop spinning.
    """
    print("Motor stopped")
    motor_pin_a.off()  # Set TA6586 IN1 LOW
    motor_pin_b.off()  # Set TA6586 IN2 LOW

def setup_motor():
    """
    Initialize the motor control system
    
    Configures TA6586 motor driver control pins and ensures motor starts in stopped state.
    """
    print("Setting up TA6586 motor control...")
    print(f"TA6586 IN1 Pin: {MOTOR_PIN_A}")
    print(f"TA6586 IN2 Pin: {MOTOR_PIN_B}")
    
    # Ensure motor starts in stopped state
    stop_motor()
    print("TA6586 motor control setup complete!")

def run_motor_cycle():
    """
    Run one complete motor cycle
    
    Executes the sequence: clockwise → stop → counterclockwise → stop
    """
    # Run motor clockwise
    rotate_clockwise()
    utime.sleep_ms(ROTATION_DURATION_MS)
    
    # Stop motor
    stop_motor()
    utime.sleep_ms(STOP_DURATION_MS)
    
    # Run motor counterclockwise
    rotate_counterclockwise()
    utime.sleep_ms(ROTATION_DURATION_MS)
    
    # Stop motor
    stop_motor()
    utime.sleep_ms(STOP_DURATION_MS)

def main():
    """
    Main function that runs the motor control demonstration
    """
    print("=== DC Motor and Fan Control Project ===")
    print("Demonstrating bidirectional motor control")
    print("Cycle: Clockwise → Stop → Counterclockwise → Stop")
    print("Press Ctrl+C to stop")
    print()
    
    # Step 1: Setup the motor control system
    setup_motor()
    print()
    
    try:
        cycle_count = 0
        print("Starting continuous motor cycles...")
        print()
        
        # Step 2: Continuous motor control loop
        while True:
            cycle_count += 1
            print(f"--- Motor Cycle #{cycle_count} ---")
            
            # Run one complete motor cycle
            run_motor_cycle()
            
            print(f"Cycle #{cycle_count} completed")
            print()
            
    except KeyboardInterrupt:
        print("\nMotor control stopped by user")
        print(f"Total cycles completed: {cycle_count}")
        
        # Ensure motor is safely stopped
        print("Ensuring motor is stopped...")
        stop_motor()
        print("Motor control system deactivated")

# Run the program
if __name__ == "__main__":
    main()