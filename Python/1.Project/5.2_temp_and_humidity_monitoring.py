"""
Simple DHT11 temperature and humidity monitoring (MicroPython)

Refactor goals:
- English comments and prints
- Replace magic numbers with named constants
- Keep the original functionality (periodic reads and printing)
- Beginner-friendly structure
"""

from machine import Pin
import utime as time
from dht import DHT11, InvalidPulseCount


# =========================
# Constants
# =========================
SENSOR_PIN = 16
INITIAL_DELAY_S = 5       # initial sensor warm-up time
READ_INTERVAL_S = 2       # interval between reads
ERROR_RETRY_DELAY_MS = 200


def main() -> None:
    # Initialize sensor
    pin = Pin(SENSOR_PIN, Pin.IN)
    sensor = DHT11(pin)

    # Allow sensor to stabilize
    print("Warming up DHT11 sensor...")
    time.sleep(INITIAL_DELAY_S)
    print("DHT11 sensor is ready.")

    try:
        while True:
            try:
                sensor.measure()
                temperature_c = sensor.temperature
                humidity_pct = sensor.humidity
                print(f"Temperature: {temperature_c} C, Humidity: {humidity_pct} %")
                time.sleep(READ_INTERVAL_S)
            except InvalidPulseCount:
                print("Bad pulse count - retrying ...")
                time.sleep_ms(ERROR_RETRY_DELAY_MS)
    except KeyboardInterrupt:
        print("Measurement stopped by user.")


if __name__ == "__main__":
    main()