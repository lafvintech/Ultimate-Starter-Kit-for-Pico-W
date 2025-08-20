import machine
import time

sdi = machine.Pin(18, machine.Pin.OUT)
rclk = machine.Pin(19, machine.Pin.OUT)
srclk = machine.Pin(20, machine.Pin.OUT)


hi_pattern = [
    0xFF, # 11111111
    0xAD, # 10101101
    0xAD, # 10101101
    0xA1, # 10100001
    0xAD, # 10101101
    0xAD, # 10101101
    0xFF, # 11111111
    0xFF  # 11111111
]

music_note = [
    0xFF, # 11111111
    0xFF, # 11110111
    0xF1, # 11110001
    0xF3, # 11110011
    0xF7, # 11110111
    0xF7, # 11110111
    0xF7, # 11110111
    0xFF  # 11111111
]

smile = [
    0xFF, # 11111111
    0xFF, # 11111111
    0xC3, # 11000011
    0xBD, # 10111101
    0xFF, # 11111111
    0x93, # 10010011
    0x93, # 10010011
    0xFF  # 11111111
]

arrow_right = [0xFF,0xF7,0xFB,0x81,0xFB,0xF7,0xFF,0xFF]
arrow_left = [0xFF,0xEF,0xDF,0x81,0xDF,0xEF,0xFF,0xFF]

def scroll_pattern_left(pattern):
    return [((row << 1) | (row >> 7)) & 0xFF for row in pattern]

def scroll_pattern_right(pattern):
    return [((row >> 1) | (row << 7)) & 0xFF for row in pattern]

def scroll_animation(pattern, direction='left', steps=8, step_delay=200):
    current = pattern
    for _ in range(steps):
        display_pattern(current, step_delay)
        if direction == 'left':
            current = scroll_pattern_left(current)
        else:
            current = scroll_pattern_right(current)

def hc595_in(dat):
    for bit in range(7, -1, -1):
        srclk.low()
        sdi.value(1 & (dat >> bit))
        srclk.high()

def hc595_out():
    rclk.high()
    rclk.low()

def display_pattern(pattern, duration_ms=1000):
    end_time = time.ticks_add(time.ticks_ms(), duration_ms)
    while time.ticks_diff(end_time, time.ticks_ms()) > 0:
        for i in range(8):
            hc595_in(pattern[i]) 
            hc595_in(0x80 >> i) 
            hc595_out()
            time.sleep_us(500) 

def main():
    while True:
        display_pattern(hi_pattern, 1500)
        
        display_pattern(music_note, 1000)
        scroll_animation(music_note, 'left', 8, 150)
        scroll_animation(music_note, 'right', 8, 150)
        
        display_pattern(smile, 1500)
        
        for _ in range(2):
            display_pattern(arrow_right, 400)
            display_pattern(arrow_left, 400)

try:
    main()
except KeyboardInterrupt:
    pass
