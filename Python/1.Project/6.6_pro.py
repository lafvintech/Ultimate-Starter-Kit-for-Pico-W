"""
Simple traffic light + 4-digit 7-segment countdown
Hardware: Raspberry Pi Pico (MicroPython)
74HC595 drives segments, 4 common-anode digits
LEDs: GP7=Red, GP8=Yellow, GP9=Green
"""

from machine import Pin, Timer
import time

# ---------- CONSTANTS ----------
# 74HC595 pins
SDI_PIN  = 18   # serial data
RCLK_PIN = 19   # latch clock
SRCLK_PIN = 20  # shift clock

# digit select pins (common anode, LOW=on)
DIGIT_PINS = (10, 13, 12, 11)

# LED pins (Red, Yellow, Green)
LED_PINS = (7, 8, 9)

# segment patterns 0-9 (abcdefgdp)
SEGMENTS = (
    0x3F, 0x06, 0x5B, 0x4F, 0x66,
    0x6D, 0x7D, 0x07, 0x7F, 0x6F
)

# light durations [Green, Yellow, Red] in seconds
DURATIONS = (30, 5, 30)

# ---------- 7-SEGMENT DISPLAY ----------
class Display:
    def __init__(self):
        self.sdi   = Pin(SDI_PIN, Pin.OUT)
        self.rclk  = Pin(RCLK_PIN, Pin.OUT)
        self.srclk = Pin(SRCLK_PIN, Pin.OUT)
        self.digit = [Pin(p, Pin.OUT) for p in DIGIT_PINS]
        for d in self.digit:
            d.value(1)           # all digits OFF

    def _shift_out(self, byte):
        self.rclk(0)
        for bit in range(7, -1, -1):
            self.srclk(0)
            self.sdi((byte >> bit) & 1)
            self.srclk(1)
        self.rclk(1)

    def show(self, value):
        for pos in range(4):
            self.digit[pos](0)               # enable digit
            digit = (value // 10**pos) % 10
            self._shift_out(SEGMENTS[digit])
            time.sleep_us(500)               # small delay for brightness
            self.digit[pos](1)               # disable digit

# ---------- TRAFFIC LIGHT ----------
class TrafficLight:
    def __init__(self):
        self.leds = [Pin(p, Pin.OUT) for p in LED_PINS]
        for l in self.leds:
            l(0)                             # all OFF

    def set(self, state):
        for l in self.leds:
            l(0)
        self.leds[state](1)

# ---------- GLOBAL STATE ----------
counter = DURATIONS[0]
state   = 0                     # 0=Green, 1=Yellow, 2=Red

def timer_cb(_):
    global counter, state
    counter -= 1
    if counter <= 0:
        state = (state + 1) % 3
        counter = DURATIONS[state]

# ---------- MAIN ----------
display = Display()
light   = TrafficLight()

Timer(period=1000, mode=Timer.PERIODIC, callback=timer_cb)

while True:
    display.show(counter)
    light.set(state)