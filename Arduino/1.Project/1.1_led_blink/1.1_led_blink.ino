/*
  Blink

  Turns an LED on for one second, then off for one second, repeatedly.

  This example uses GPIO 15 for the LED connection on Raspberry Pi Pico.
  Connect the LED with a 220 ohm resistor in series.
*/

// Pin 15 has the LED connected
const int led = 15;

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize the digital pin as an output.
  pinMode(led, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(led, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(1000);               // wait for a second
  digitalWrite(led, LOW);    // turn the LED off by making the voltage LOW
  delay(1000);               // wait for a second
}