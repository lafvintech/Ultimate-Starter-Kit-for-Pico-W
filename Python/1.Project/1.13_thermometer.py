"""
Digital Thermometer

Reads temperature from a thermistor and displays 
the temperature in both Celsius and Fahrenheit.
"""

import machine
import utime
import math

# Pin and sensor constants
THERMISTOR_PIN = 28              # thermistor connected to pin 28 (ADC)
BETA_VALUE = 3950                # beta coefficient of the thermistor
PULLUP_RESISTANCE = 10000        # pull-up resistor value in Ohms
UPDATE_INTERVAL = 1000           # reading interval in milliseconds

# Temperature calculation constants
ROOM_TEMP_KELVIN = 298.15        # room temperature in Kelvin (25°C)
KELVIN_OFFSET = 273.15           # conversion offset from Celsius to Kelvin
ADC_MAX_VALUE = 65535            # 16-bit ADC maximum value
SUPPLY_VOLTAGE = 3.3             # supply voltage

# Initialize thermistor ADC
thermistor = machine.ADC(THERMISTOR_PIN)

def read_and_display_temperature():
    """Read thermistor and calculate temperature"""
    # Read raw analog value from thermistor
    analog_value = thermistor.read_u16()
    
    # Calculate temperature using the same logic as reference code
    # Convert ADC reading to voltage (0-65535 maps to 0-3.3V)
    voltage = SUPPLY_VOLTAGE * float(analog_value) / ADC_MAX_VALUE
    
    # Calculate thermistor resistance using voltage divider formula
    thermistor_resistance = PULLUP_RESISTANCE * voltage / (SUPPLY_VOLTAGE - voltage)
    
    # Calculate temperature using Beta equation
    temp_kelvin = 1.0 / (1.0 / ROOM_TEMP_KELVIN + math.log(thermistor_resistance / PULLUP_RESISTANCE) / BETA_VALUE)
    temp_celsius = temp_kelvin - KELVIN_OFFSET
    
    # Convert to Fahrenheit
    temp_fahrenheit = (temp_celsius * 1.8) + 32.0
    
    # Display temperature readings
    print(f"Temperature: {temp_celsius:.1f}°C ({temp_fahrenheit:.1f}°F)", end="")
    
    # Show temperature category
    if temp_celsius < 15:
        print(" - Cold")
    elif temp_celsius < 25:
        print(" - Cool")
    elif temp_celsius < 30:
        print(" - Comfortable")
    else:
        print(" - Warm")

def main():
    """Main function"""
    print("=== Digital Thermometer ===")
    print("Reading temperature from thermistor...")
    print()
    
    while True:
        # Read temperature and display results
        read_and_display_temperature()
        
        # Wait before next reading
        utime.sleep_ms(UPDATE_INTERVAL)

if __name__ == "__main__":
    main()