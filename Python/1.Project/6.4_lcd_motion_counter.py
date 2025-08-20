from lcd1602 import LCD
from machine import I2C, Pin
import utime as time

pir = Pin(16, Pin.IN) 
i2c = I2C(1, sda=Pin(6), scl=Pin(7), freq=400000)
lcd = LCD(i2c)

motion_count = 0
last_detection_time = 0

def display_status(motion_detected, count):
    lcd.clear()
    if motion_detected:
        lcd.message("Motion Detected!\nCount: {}".format(count))
    else:
        lcd.message("Monitoring...\nCount: {}".format(count))

# Main loop
print("PIR Sensor initializing...")
time.sleep(2)  # Wait for PIR sensor to stabilize
lcd.message("System Ready\nStarting...")
time.sleep(2)

while True:
    try:
        current_time = time.ticks_ms()
        
        if pir.value() == 1:  # Motion detected
            # Check if it's a new motion (at least 2 seconds since last detection)
            if time.ticks_diff(current_time, last_detection_time) > 2000:
                motion_count += 1
                last_detection_time = current_time
                display_status(True, motion_count)
                print("Motion detected! Count:", motion_count)
                time.sleep(1)
        else:
            # No motion detected
            if time.ticks_diff(current_time, last_detection_time) > 2000:
                display_status(False, motion_count)
        
        time.sleep_ms(100)  # Short delay to avoid too frequent detection
        
    except Exception as e:
        print("Error:", e)
        lcd.clear()
        lcd.message("Error occurred\nRestarting...")
        time.sleep(2)
        continue