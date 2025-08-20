from time import sleep_ms
from machine import Pin

led=Pin(15,Pin.OUT) #create LED object from pin2,Set Pin2 to output
try:
    while True:
        led.value(1)        #Set led turn on
        sleep_ms(200)
        led.value(0)        #Set led turn off
        sleep_ms(200)
except:
    pass 