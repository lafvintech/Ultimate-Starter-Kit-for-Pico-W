# 6.8_morse_code_generator.py
# A professional, feature-rich Morse code generator for MicroPython,
# inspired by a well-structured Raspberry Pi example.

from machine import Pin, PWM
import time
import sys

# --- Configuration ---
BUZZER_PIN = 15      # Pin for the buzzer
LED_PIN = 14         # Pin for the LED
DOT_DURATION = 0.15  # Base time unit for a dot (seconds)

# --- Morse Code Dictionary (Standard Notation) ---
MORSE_DICTIONARY = {
    'A': '.-',   'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.',  'H': '....', 'I': '..',  'J': '.---',
    'K': '-.-',  'L': '.-..', 'M': '--',   'N': '-.',  'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.',  'S': '...', 'T': '-',
    'U': '..-',  'V': '...-', 'W': '.--',  'X': '-..-', 'Y': '-.--',
    'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '?': '..--..', '/': '-..-.', ',': '--..--', '.': '.-.-.-',
    ';': '-.-.-.', '!': '-.-.--', '@': '.--.-.', ':': '---...'
}

class MorseCodeGenerator:
    """
    A class to handle Morse code generation with LED and Buzzer feedback.
    """
    def __init__(self, led_pin, buzzer_pin, dot_duration):
        """Initializes the generator and hardware."""
        self.dot_duration = dot_duration
        self.dash_duration = dot_duration * 3  # A dash is 3x a dot
        self.symbol_pause = dot_duration       # Pause between dots/dashes is 1x dot
        self.letter_pause = dot_duration * 3   # Pause between letters is 3x dot
        self.word_pause = dot_duration * 7     # Pause between words is 7x dot

        self.led = Pin(led_pin, Pin.OUT)
        self.buzzer = PWM(Pin(buzzer_pin))
        self.buzzer.freq(1000)  # Set a pleasant frequency
        self.cleanup() # Ensure outputs are off

    def signal_on(self):
        """Turns the LED and Buzzer on."""
        self.led.value(1)
        self.buzzer.duty_u16(32768)  # 50% duty cycle for sound

    def signal_off(self):
        """Turns the LED and Buzzer off."""
        self.led.value(0)
        self.buzzer.duty_u16(0)

    def play_signal(self, duration):
        """Plays a signal (dot or dash) for a given duration."""
        self.signal_on()
        time.sleep(duration)
        self.signal_off()
        time.sleep(self.symbol_pause)

    def play_morse_message(self, message):
        """Converts and plays an entire message in Morse code."""
        print(f"\n🎵 Playing Morse code for: \"{message}\"")
        print("--- Morse Code Output ---")
        
        for char in message.upper():
            if char == ' ':
                print("   (space)")
                time.sleep(self.word_pause - self.letter_pause) # Account for upcoming letter pause
                continue

            pattern = MORSE_DICTIONARY.get(char)
            if pattern is None:
                print(f"⚠️ Character '{char}' not supported, skipping.")
                continue

            print(f"📡 {char} -> {pattern}")
            for symbol in pattern:
                if symbol == '.':
                    self.play_signal(self.dot_duration)
                elif symbol == '-':
                    self.play_signal(self.dash_duration)
            
            time.sleep(self.letter_pause - self.symbol_pause) # Pause between letters

        print("✅ Transmission complete!\n")

    def display_morse_chart(self):
        """Displays a formatted Morse code reference chart."""
        print("\n" + "="*50)
        print("📊 Morse Code Reference Chart:")
        print("="*50)
        
        sorted_items = sorted(MORSE_DICTIONARY.items())
        count = 0
        for char, code in sorted_items:
            print(f"{char}: {code:<8}", end="")
            count += 1
            if count % 5 == 0:
                print()
        print("\n" + "="*50 + "\n")

    def cleanup(self):
        """Turns off all hardware outputs."""
        print("\n🧹 Shutting down... Turning off signals.")
        self.signal_off()

    def run(self):
        """The main interactive loop for the generator."""
        print("\n🎯 Morse Code Generator is Active!")
        print("   - Type a message and press Enter to play.")
        print("   - Type 'chart' to display the Morse code reference.")
        print("   - Press Ctrl+C to exit.\n")
        
        while True:
            try:
                message = input("💬 Enter message (or 'chart'): ").strip()
                if not message:
                    continue
                
                if message.lower() == 'chart':
                    self.display_morse_chart()
                else:
                    self.play_morse_message(message)
            
            except (KeyboardInterrupt, EOFError):
                break
        
        self.cleanup()
        print("✅ Goodbye!")

def main():
    """Main function to start the application."""
    print("\n" + "="*30)
    print("=== Morse Code Generator ===")
    print("="*30)
    
    generator = MorseCodeGenerator(
        led_pin=LED_PIN,
        buzzer_pin=BUZZER_PIN,
        dot_duration=DOT_DURATION
    )
    generator.run()

if __name__ == '__main__':
    main()