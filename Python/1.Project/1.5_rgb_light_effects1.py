from machine import Pin, PWM
from random import randint
import time

pins = [13, 14, 15]

pwm0 = PWM(Pin(pins[0]), freq=10000)
pwm1 = PWM(Pin(pins[1]), freq=10000)
pwm2 = PWM(Pin(pins[2]), freq=10000)

def map_value(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def setColor(r, g, b):
    pwm0.duty_u16(65535 - map_value(r, 0, 1023, 0, 65535))
    pwm1.duty_u16(65535 - map_value(g, 0, 1023, 0, 65535))
    pwm2.duty_u16(65535 - map_value(b, 0, 1023, 0, 65535))

try:
    while True:
        red = randint(0, 1023)
        green = randint(0, 1023)
        blue = randint(0, 1023)
        setColor(red, green, blue)
        time.sleep_ms(200)
        
except KeyboardInterrupt:
    pwm0.deinit()
    pwm1.deinit()
    pwm2.deinit()
