# 6.12_rfid_jukebox.py
# A professional, feature-rich RFID Music Player for MicroPython.
#
# This system continuously waits for an RFID card and plays a musical score
# stored on it. It provides interactive visual feedback on a WS2812 LED strip,
# handles errors gracefully, and is structured for easy maintenance.

from mfrc522 import SimpleMFRC522
from ws2812 import WS2812
import machine
import time
import urandom

# --- Configuration ---
# Hardware Pins
WS2812_PIN = 0
BUZZER_PIN = 15
RFID_SCK_PIN = 18
RFID_MISO_PIN = 16
RFID_MOSI_PIN = 19
RFID_CS_PIN = 17
RFID_RST_PIN = 9

# LED & Sound Config
NUM_LEDS = 8
NOTE_DURATION_MS = 250
# A nice color palette for the VU meter effect (in GRB format for WS2812)
VU_METER_COLORS = [
    0x00FF00, 0x33FF00, 0x66FF00, 0x99FF00,
    0xFFFF00, 0xFF9900, 0xFF6600, 0xFF0000
]

# Note Frequencies (in Hz)
NOTES = {
    'C': 262, 'D': 294, 'E': 330, 'F': 349,
    'G': 392, 'A': 440, 'B': 494, 'N': 523 # 'N' for next octave C
}
NOTE_SEQUENCE = ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'N']

class RFIDJukebox:
    """
    Manages all functionality for the RFID Jukebox system.
    """
    def __init__(self):
        """Initializes all hardware components."""
        print("🔧 Initializing RFID Jukebox...")
        
        # WS2812 LED Strip
        self.led_strip = WS2812(machine.Pin(WS2812_PIN), NUM_LEDS)
        
        # MFRC522 RFID Reader
        self.reader = SimpleMFRC522(
            spi_id=0, sck=RFID_SCK_PIN, miso=RFID_MISO_PIN,
            mosi=RFID_MOSI_PIN, cs=RFID_CS_PIN, rst=RFID_RST_PIN
        )
        
        # Buzzer (PWM)
        self.buzzer = machine.PWM(machine.Pin(BUZZER_PIN))
        
        self.cleanup() # Ensure all outputs are off
        print("✅ Jukebox Ready! Please scan a card.")

    def play_note(self, note_char):
        """Plays a single note with corresponding visual feedback."""
        try:
            # Find the note's frequency and its position for the VU meter
            note_index = NOTE_SEQUENCE.index(note_char)
            frequency = NOTES[note_char]

            # --- Visual Feedback (VU Meter) ---
            for i in range(NUM_LEDS):
                if i <= note_index:
                    self.led_strip[i] = VU_METER_COLORS[i]
                else:
                    self.led_strip[i] = 0 # Off
            self.led_strip.write()

            # --- Audio Feedback ---
            self.buzzer.freq(frequency)
            self.buzzer.duty_u16(30000) # 50% duty cycle
            time.sleep_ms(NOTE_DURATION_MS)
            self.buzzer.duty_u16(0) # Stop sound
            
        except (ValueError, KeyError):
            print(f"⚠️ Warning: Character '{note_char}' is not a valid note. Skipping.")
            # Flash all LEDs red for an error
            for i in range(NUM_LEDS):
                self.led_strip[i] = 0xFF0000 # Red
            self.led_strip.write()
            time.sleep_ms(NOTE_DURATION_MS)


    def play_score(self, text):
        """Plays an entire musical score from a text string."""
        if not text:
            print("Card is empty. Nothing to play.")
            return
            
        print(f"🎵 Playing score: \"{text}\"")
        clean_text = text.replace(' ', '').upper()
        
        for note_char in clean_text:
            self.play_note(note_char)
            time.sleep_ms(50) # Short pause between notes
            
        print("✅ Score finished.")

    def cleanup(self):
        """Turns off all hardware outputs for a safe state."""
        self.buzzer.duty_u16(0)
        for i in range(NUM_LEDS):
            self.led_strip[i] = 0
        self.led_strip.write()

    def run(self):
        """The main continuous loop to read cards and play music."""
        while True:
            self.cleanup()
            print("\nWaiting for a card...")
            
            # This read() call will block until a card is present
            card_id, text = self.reader.read()
            
            print("-" * 30)
            print(f"💳 Card Scanned! ID: {card_id}")
            self.play_score(text)

def main():
    """Main function to start the application."""
    jukebox = RFIDJukebox()
    
    try:
        jukebox.run()
    except KeyboardInterrupt:
        print("\n🛑 Program interrupted by user.")
    finally:
        jukebox.cleanup()
        print("🧹 System shut down cleanly.")

if __name__ == '__main__':
    main()