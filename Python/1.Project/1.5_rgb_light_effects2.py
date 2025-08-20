from machine import Pin, PWM
import time

pins = [13,14,15]

pwm0 = PWM(Pin(pins[0]), freq=1000)
pwm1 = PWM(Pin(pins[1]), freq=1000)
pwm2 = PWM(Pin(pins[2]), freq=1000)

red = 0
green = 0
blue = 0

def map_value(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def setColor():
    pwm0.duty_u16(map_value(red, 0, 255, 0, 65535))
    pwm1.duty_u16(map_value(green, 0, 255, 0, 65535))
    pwm2.duty_u16(map_value(blue, 0, 255, 0, 65535))

def wheel(pos):
    global red, green, blue
    WheelPos = pos % 256
    
    if WheelPos < 85:
        red = 255 - WheelPos * 3
        green = WheelPos * 3
        blue = 0
    elif WheelPos < 170:
        WheelPos -= 85
        red = 0
        green = 255 - WheelPos * 3
        blue = WheelPos * 3
    else:
        WheelPos -= 170
        red = WheelPos * 3
        green = 0
        blue = 255 - WheelPos * 3
    
    red = max(0, min(255, red))
    green = max(0, min(255, green))
    blue = max(0, min(255, blue))

try:
    while True:
        for i in range(0, 256):
            wheel(i)
            setColor()
            time.sleep_ms(15)

            
except KeyboardInterrupt:
    pwm0.deinit()
    pwm1.deinit()
    pwm2.deinit()
