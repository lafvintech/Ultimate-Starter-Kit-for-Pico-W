// Define pins
const int SDI_PIN = 18;   // Data input
const int RCLK_PIN = 19;  // Storage register clock
const int SRCLK_PIN = 20; // Shift register clock

// Define pattern arrays
const byte hi_pattern[] = {
    0xFF, // 11111111
    0xAD, // 10101101
    0xAD, // 10101101
    0xA1, // 10100001
    0xAD, // 10101101
    0xAD, // 10101101
    0xFF, // 11111111
    0xFF  // 11111111
};

const byte music_note[] = {
    0xFF, // 11111111
    0xFF, // 11110111
    0xF1, // 11110001
    0xF3, // 11110011
    0xF7, // 11110111
    0xF7, // 11110111
    0xF7, // 11110111
    0xFF  // 11111111
};

const byte smile[] = {
    0xFF, // 11111111
    0xFF, // 11111111
    0xC3, // 11000011
    0xBD, // 10111101
    0xFF, // 11111111
    0x93, // 10010011
    0x93, // 10010011
    0xFF  // 11111111
};

const byte arrow_right[] = {0xFF,0xF7,0xFB,0x81,0xFB,0xF7,0xFF,0xFF};
const byte arrow_left[] = {0xFF,0xEF,0xDF,0x81,0xDF,0xEF,0xFF,0xFF};

void setup() {
  pinMode(SDI_PIN, OUTPUT);
  pinMode(RCLK_PIN, OUTPUT);
  pinMode(SRCLK_PIN, OUTPUT);
}

// Send data to 74HC595
void hc595_in(byte dat) {
  for (int bit = 7; bit >= 0; bit--) {
    digitalWrite(SRCLK_PIN, LOW);
    digitalWrite(SDI_PIN, (dat >> bit) & 0x01);
    digitalWrite(SRCLK_PIN, HIGH);
  }
}

// Output data to storage register
void hc595_out() {
  digitalWrite(RCLK_PIN, HIGH);
  digitalWrite(RCLK_PIN, LOW);
}

// Display pattern
void display_pattern(const byte pattern[], unsigned long duration_ms) {
  unsigned long start_time = millis();
  while (millis() - start_time < duration_ms) {
    for (int i = 0; i < 8; i++) {
      hc595_in(pattern[i]);
      hc595_in(0x80 >> i);
      hc595_out();
      delayMicroseconds(500);
    }
  }
}

// Scroll pattern to the left
void scroll_pattern_left(byte result[], const byte pattern[]) {
  for (int i = 0; i < 8; i++) {
    result[i] = ((pattern[i] << 1) | (pattern[i] >> 7)) & 0xFF;
  }
}

// Scroll pattern to the right
void scroll_pattern_right(byte result[], const byte pattern[]) {
  for (int i = 0; i < 8; i++) {
    result[i] = ((pattern[i] >> 1) | (pattern[i] << 7)) & 0xFF;
  }
}

// Scroll animation
void scroll_animation(const byte pattern[], char direction, int steps, int step_delay) {
  byte current[8];
  memcpy(current, pattern, 8);
  
  for (int step = 0; step < steps; step++) {
    display_pattern(current, step_delay);
    byte temp[8];
    if (direction == 'l') {
      scroll_pattern_left(temp, current);
    } else {
      scroll_pattern_right(temp, current);
    }
    memcpy(current, temp, 8);
  }
}

void loop() {
  // Display "HI" pattern
  display_pattern(hi_pattern, 1500);

  // Display music note pattern and scroll
  display_pattern(music_note, 1000);
  scroll_animation(music_note, 'l', 8, 150);
  scroll_animation(music_note, 'r', 8, 150);

  // Display smiley face
  display_pattern(smile, 1500);

  // Display arrow animation
  for (int i = 0; i < 2; i++) {
    display_pattern(arrow_right, 400);
    display_pattern(arrow_left, 400);
  }
}