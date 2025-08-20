/*
 * MFRC522 RFID Card Writer Project (Arduino)
 * 
 * This project writes text data to RFID cards using the MFRC522 module.
 * Features a user-friendly interface for card programming and verification.
 * 
 * Hardware Requirements:
 * - Arduino-compatible board
 * - MFRC522 RFID module
 * - RFID cards (MIFARE Classic 1K)
 */

#include <SPI.h>
#include <MFRC522.h>

// Pin Configuration Constants
#define RFID_RST_PIN          9       // Reset pin for MFRC522
#define RFID_SS_PIN           17      // Slave Select (CS) pin for MFRC522

// Communication Constants
#define SERIAL_BAUD_RATE      115200  // Serial communication speed
#define SERIAL_TIMEOUT_MS     10      // Serial initialization timeout

// RFID Writing Constants
#define INPUT_BUFFER_SIZE     34      // Buffer size for input data
#define MAX_INPUT_LENGTH      30      // Maximum input string length
#define CARD_SECTION          0       // Default card section to write
#define INPUT_TERMINATOR      '#'     // Character to end input

// Create MFRC522 instance
MFRC522 rfidReader(RFID_SS_PIN, RFID_RST_PIN);


void setup() {
  Serial.begin(SERIAL_BAUD_RATE);
  while (!Serial) {
    delay(SERIAL_TIMEOUT_MS);
  }
  
  initializeRFID();
  displayWelcomeMessage();
}

void loop() {
  byte inputBuffer[INPUT_BUFFER_SIZE];
  byte inputLength;
  
  // Read user input from serial
  inputLength = Serial.readBytesUntil(INPUT_TERMINATOR, (char*)inputBuffer, MAX_INPUT_LENGTH);
  
  if (inputLength == 0) {
    return; // No input received, continue waiting
  }
  
  // Pad buffer with spaces to fill the card section
  for (byte i = inputLength; i < MAX_INPUT_LENGTH; i++) {
    inputBuffer[i] = ' ';
  }
  
  // Display card placement prompt
  Serial.println("\n" + String("=").substring(0, 40));
  Serial.println("Place an RFID card near the sensor...");
  Serial.println(String("=").substring(0, 40));
  
  // Wait for card and write data
  waitForCardAndGetInfo();
  writeDataToCard(inputBuffer);
}


// Initialize RFID reader hardware
void initializeRFID() {
  SPI.begin();
  rfidReader.PCD_Init();
}

// Display welcome message and instructions
void displayWelcomeMessage() {
  Serial.println(String("=").substring(0, 50));
  Serial.println("    RFID CARD WRITER");
  Serial.println(String("=").substring(0, 50));
  Serial.println("This program writes text data to RFID cards.");
  Serial.println(String("=").substring(0, 50));
  Serial.println("\nWriting mode active...");
  Serial.println("Type your message and end with '#' to write to card");
  Serial.println("Example: Hello World#");
  Serial.println(String("-").substring(0, 50));
}

// Wait for card placement and display card information
void waitForCardAndGetInfo() {
  // Wait for a new card to be present
  while (!rfidReader.PICC_IsNewCardPresent()) {
    // Keep waiting
  }
  
  // Select one of the cards
  while (!rfidReader.PICC_ReadCardSerial()) {
    // Keep waiting
  }
  
  Serial.println("\nCARD DETECTED!");
  Serial.println("+" + String("-").substring(0, 48) + "+");
  
  // Display card UID
  Serial.print("| Card ID:    ");
  for (byte i = 0; i < rfidReader.uid.size; i++) {
    Serial.print(rfidReader.uid.uidByte[i] < 0x10 ? " 0" : " ");
    Serial.print(rfidReader.uid.uidByte[i], HEX);
  }
  
  // Pad the line to make it align properly
  int spaces = 32 - (rfidReader.uid.size * 3);
  for (int i = 0; i < spaces; i++) {
    Serial.print(" ");
  }
  Serial.println(" |");
  
  // Display card type
  MFRC522::PICC_Type cardType = rfidReader.PICC_GetType(rfidReader.uid.sak);
  String typeName = String(rfidReader.PICC_GetTypeName(cardType));
  Serial.print("| Card Type:  " + typeName);
  
  // Pad the line
  spaces = 32 - typeName.length();
  for (int i = 0; i < spaces; i++) {
    Serial.print(" ");
  }
  Serial.println(" |");
  Serial.println("+" + String("-").substring(0, 48) + "+");
}

// Write data to RFID card with error handling and status display
void writeDataToCard(byte* dataBuffer) {
  MFRC522::StatusCode status;
  MFRC522::MIFARE_Key authKey;
  
  // Initialize default authentication key (all 0xFF)
  for (byte i = 0; i < 6; i++) {
    authKey.keyByte[i] = 0xFF;
  }
  
  // Calculate block addresses for section 0 (blocks 1 and 2)
  byte firstBlock = CARD_SECTION * 3 + 1;
  byte secondBlock = firstBlock + 1;
  
  Serial.println("\nWriting data to card...");
  
  // Write first 16 bytes to first block
  if (authenticateAndWriteBlock(firstBlock, &authKey, dataBuffer)) {
    Serial.println("Block 1 write: SUCCESS");
    
    // Write remaining 16 bytes to second block
    if (authenticateAndWriteBlock(secondBlock, &authKey, &dataBuffer[16])) {
      Serial.println("Block 2 write: SUCCESS");
      Serial.println("\n" + String("=").substring(0, 40));
      Serial.println("Write operation completed successfully!");
      Serial.println("Card programming finished.");
      Serial.println(String("=").substring(0, 40));
    } else {
      Serial.println("Block 2 write: FAILED");
    }
  } else {
    Serial.println("Block 1 write: FAILED");
  }
  
  // Clean up - halt card and stop encryption
  rfidReader.PICC_HaltA();
  rfidReader.PCD_StopCrypto1();
  
  Serial.println("\nReady for next write operation...");
  Serial.println("Type your next message ending with '#'");
}

// Authenticate and write a single block of data
bool authenticateAndWriteBlock(byte blockNumber, MFRC522::MIFARE_Key* key, byte* data) {
  MFRC522::StatusCode status;
  
  // Authenticate with the card
  status = rfidReader.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, blockNumber, key, &(rfidReader.uid));
  if (status != MFRC522::STATUS_OK) {
    Serial.print("Authentication failed for block ");
    Serial.print(blockNumber);
    Serial.print(": ");
    Serial.println(rfidReader.GetStatusCodeName(status));
    return false;
  }
  
  // Write data to the block
  status = rfidReader.MIFARE_Write(blockNumber, data, 16);
  if (status != MFRC522::STATUS_OK) {
    Serial.print("Write failed for block ");
    Serial.print(blockNumber);
    Serial.print(": ");
    Serial.println(rfidReader.GetStatusCodeName(status));
    return false;
  }
  
  return true;
}
