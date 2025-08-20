import machine
import time
from machine import Timer

# Traffic light timing constants (seconds)
GREEN_TIME = 30
YELLOW_TIME = 5  
RED_TIME = 30
LIGHT_DURATIONS = [GREEN_TIME, YELLOW_TIME, RED_TIME]

# Traffic light states
STATE_GREEN = 0
STATE_YELLOW = 1
STATE_RED = 2
STATE_NAMES = ["GREEN", "YELLOW", "RED"]

# 7-segment display constants
SEGMENT_CODES = [0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 0x07, 0x7f, 0x6f]
DISPLAY_CLEAR = 0x00
TIMING_DELAY_US = 200
MAX_DIGITS = 4

# Pin definitions
# 74HC595 shift register pins
SDI_PIN = 18    # Serial Data Input
RCLK_PIN = 19   # Register Clock (Latch)
SRCLK_PIN = 20  # Shift Register Clock

# 7-segment display digit control pins
DIGIT_PINS = [10, 13, 12, 11]

# Traffic light LED pins
LED_RED_PIN = 7
LED_YELLOW_PIN = 8  
LED_GREEN_PIN = 9
LED_PINS = [LED_RED_PIN, LED_YELLOW_PIN, LED_GREEN_PIN]



# Initialize hardware pins
sdi = machine.Pin(SDI_PIN, machine.Pin.OUT)
rclk = machine.Pin(RCLK_PIN, machine.Pin.OUT)
srclk = machine.Pin(SRCLK_PIN, machine.Pin.OUT)

# Initialize digit control pins
digit_pins = []
for pin_num in DIGIT_PINS:
    digit_pins.append(machine.Pin(pin_num, machine.Pin.OUT))

# === 7-Segment Display Functions (Core - Keep Original Logic) ===

def select_digit(digit):
    """Select which digit (0-3) to display"""
    for i in range(MAX_DIGITS):
        digit_pins[i].value(1)  # Turn off all digits
    digit_pins[digit].value(0)  # Turn on selected digit

def clear_display():
    """Clear the display by sending clear code to shift register"""
    shift_register_send(DISPLAY_CLEAR)

def shift_register_send(data):
    """Send data to 74HC595 shift register"""
    rclk.low()
    time.sleep_us(TIMING_DELAY_US)
    for bit in range(7, -1, -1):
        srclk.low()
        time.sleep_us(TIMING_DELAY_US)
        bit_value = 1 & (data >> bit)
        sdi.value(bit_value)
        time.sleep_us(TIMING_DELAY_US)
        srclk.high()
        time.sleep_us(TIMING_DELAY_US)
    time.sleep_us(TIMING_DELAY_US)
    rclk.high()



# === Traffic Light LED Functions (Core - Keep Original Logic) ===

# Initialize LED pins
led_pins = []
for pin_num in LED_PINS:
    led_pins.append(machine.Pin(pin_num, machine.Pin.OUT))

def set_traffic_light(state):
    """Turn on the specified traffic light LED"""
    for i in range(3):
        led_pins[i].value(0)  # Turn off all LEDs
    led_pins[state].value(1)  # Turn on selected LED



# === System State Variables ===
counter = LIGHT_DURATIONS[STATE_GREEN]
current_state = STATE_GREEN

def timer_callback(timer):
    """Timer interrupt handler for traffic light state management"""
    global counter, current_state
    
    counter -= 1
    if counter <= 0:
        current_state = (current_state + 1) % 3
        counter = LIGHT_DURATIONS[current_state]

# Initialize timer for 1-second intervals
timer = Timer(period=1000, mode=Timer.PERIODIC, callback=timer_callback)

def display_number(number):
    """Display complete number on 7-segment display (original working logic)"""
    select_digit(0)
    shift_register_send(SEGMENT_CODES[number % 10])
    
    select_digit(1)
    shift_register_send(SEGMENT_CODES[number % 100 // 10])
    
    select_digit(2)
    shift_register_send(SEGMENT_CODES[number % 1000 // 100])
    
    select_digit(3)
    shift_register_send(SEGMENT_CODES[number % 10000 // 1000])

# === Main Control Loop ===
while True:
    display_number(counter)
    set_traffic_light(current_state)