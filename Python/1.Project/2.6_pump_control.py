import machine
import utime

motor1A = machine.Pin(14, machine.Pin.OUT)
motor2A = machine.Pin(15, machine.Pin.OUT)
switch = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)

pump_state = False
last_switch_state = 1

def pump_on():
    motor1A.high()
    motor2A.low()
    
def pump_off():
    motor1A.low()
    motor2A.low()

pump_off()

while True:
    current_switch_state = switch.value()
    
    if current_switch_state == 0 and last_switch_state == 1:
        utime.sleep_ms(20)
        if switch.value() == 0: 
            pump_state = not pump_state
            if pump_state:
                pump_on()
                print("power on")
            else:
                pump_off()
                print("power off")
    
    last_switch_state = current_switch_state
    utime.sleep_ms(50)
