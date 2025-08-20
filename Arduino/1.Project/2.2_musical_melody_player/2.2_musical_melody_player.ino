/*
  Musical Melody Player

  Plays "Twinkle Twinkle Little Star" melody using 
  tone generation on a buzzer or speaker.
*/

// Musical note frequencies (in Hz)
const int NOTE_C4 = 262;    // Do
const int NOTE_D4 = 294;    // Re  
const int NOTE_E4 = 330;    // Mi
const int NOTE_F4 = 349;    // Fa
const int NOTE_G4 = 392;    // Sol
const int NOTE_A4 = 440;    // La
const int NOTE_B4 = 494;    // Ti
const int NOTE_C5 = 523;    // Do (high)

// Pin and timing constants
const int BUZZER_PIN = 15;          // buzzer connected to pin 15
const int MELODY_LENGTH = 14;       // number of notes in melody
const int REPEAT_DELAY = 2000;      // delay before repeating melody

// "Twinkle Twinkle Little Star" melody
int melody[MELODY_LENGTH] = {
  NOTE_C4, NOTE_C4, NOTE_G4, NOTE_G4,  // Twin-kle twin-kle
  NOTE_A4, NOTE_A4, NOTE_G4,           // lit-tle star
  NOTE_F4, NOTE_F4, NOTE_E4, NOTE_E4,  // How I won-der  
  NOTE_D4, NOTE_D4, NOTE_C4            // what you are
};

// Note durations (4 = quarter note, 8 = eighth note, 2 = half note)
int noteDurations[MELODY_LENGTH] = {
  4, 4, 4, 4,  // quarter notes
  4, 4, 2,     // quarter, quarter, half
  4, 4, 4, 4,  // quarter notes  
  4, 4, 2      // quarter, quarter, half
};

void setup() {
  // Initialize serial communication
  Serial.begin(115200);
  Serial.println("=== Musical Melody Player ===");
  Serial.println("Playing: Twinkle Twinkle Little Star");
  Serial.println();
  
  // Play the melody once on startup
  playMelody();
}

void loop() {
  // Wait and then repeat the melody
  Serial.println("Playing melody again...");
  delay(REPEAT_DELAY);
  playMelody();
}

// Function to play the complete melody
void playMelody() {
  Serial.println("♪ Now playing: Twinkle Twinkle Little Star ♪");
  
  // Play each note in the melody
  for (int noteIndex = 0; noteIndex < MELODY_LENGTH; noteIndex++) {
    // Calculate note duration
    int noteDuration = 1000 / noteDurations[noteIndex];
    
    // Play the note
    tone(BUZZER_PIN, melody[noteIndex], noteDuration);
    
    // Show current note being played
    Serial.print("Note ");
    Serial.print(noteIndex + 1);
    Serial.print("/");
    Serial.print(MELODY_LENGTH);
    Serial.print(": ");
    Serial.print(melody[noteIndex]);
    Serial.println("Hz");
    
    // Pause between notes (note duration + 30% for clear separation)
    int pauseBetweenNotes = noteDuration * 1.30;
    delay(pauseBetweenNotes);
    
    // Stop the tone
    noTone(BUZZER_PIN);
  }
  
  Serial.println("Melody complete!");
  Serial.println();
}