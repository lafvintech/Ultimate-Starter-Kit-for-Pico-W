import machine
import utime

pin_nums = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
pins = [machine.Pin(p, machine.Pin.OUT) for p in pin_nums]

pwms = [machine.PWM(pin, freq=1000) for pin in pins]

MAX_DUTY = 65535
steps = 32
breath_pattern = []
for i in range(steps):
    duty = int(MAX_DUTY * (1 - abs((i - steps/2)/(steps/2))))
    breath_pattern.append(duty)

def cleanup():
    for pwm in pwms:
        pwm.deinit()

try:
    while True:
        for step in range(steps):
            for i, pwm in enumerate(pwms):
                phase = (step - i * 2) % steps 
                pwm.duty_u16(breath_pattern[phase])
            utime.sleep_ms(50)
            
except KeyboardInterrupt:
    cleanup()
