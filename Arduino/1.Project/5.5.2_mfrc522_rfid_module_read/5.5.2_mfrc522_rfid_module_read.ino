/*
 * MFRC522 RFID Card Reader Project (Arduino)
 * 
 * This project reads text data from RFID cards using the MFRC522 module.
 * Features a user-friendly interface inspired by professional implementations.
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

// RFID Reading Constants
#define CARD_SECTION          0       // Default card section to read
#define READ_DELAY_MS         1000    // Delay between card reads
#define BLOCK_SIZE            16      // Size of each MIFARE block in bytes

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
  Serial.println("\nReading mode active...");
  Serial.println("Please place an RFID card near the sensor.");
  
  waitForCardAndGetInfo();
  String cardData = readCardData();
  displayReadResults(cardData);
  
  delay(READ_DELAY_MS);
}


// Initialize RFID reader hardware
void initializeRFID() {
  SPI.begin();
  rfidReader.PCD_Init();
}

// Display welcome message and instructions
void displayWelcomeMessage() {
  Serial.println(String("=").substring(0, 50));
  Serial.println("    RFID CARD READER");
  Serial.println(String("=").substring(0, 50));
  Serial.println("This program reads data from RFID cards.");
  Serial.println(String("=").substring(0, 50));
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

// Read data from RFID card
String readCardData() {
  return readCardSection(CARD_SECTION);
}

// Read data from specific card section with error handling
String readCardSection(byte section) {
  MFRC522::StatusCode status;
  MFRC522::MIFARE_Key authKey;
  
  // Initialize default authentication key (all 0xFF)
  for (byte i = 0; i < 6; i++) {
    authKey.keyByte[i] = 0xFF;
  }
  
  // Calculate block address for the section
  byte blockNumber = section * 3 + 1;
  byte dataBuffer[18];
  byte bufferLength = 18;
  
  // Authenticate with the card
  status = rfidReader.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, blockNumber, &authKey, &(rfidReader.uid));
  if (status != MFRC522::STATUS_OK) {
    Serial.print("Authentication failed: ");
    Serial.println(rfidReader.GetStatusCodeName(status));
    return "";
  }
  
  // Read data from the block
  status = rfidReader.MIFARE_Read(blockNumber, dataBuffer, &bufferLength);
  if (status != MFRC522::STATUS_OK) {
    Serial.print("Reading failed: ");
    Serial.println(rfidReader.GetStatusCodeName(status));
    return "";
  }
  
  // Clean up - halt card and stop encryption
  rfidReader.PICC_HaltA();
  rfidReader.PCD_StopCrypto1();
  
  // Convert byte data to string
  String result = "";
  for (uint8_t i = 0; i < BLOCK_SIZE; i++) {
    result += String((char)dataBuffer[i]);
  }
  
  return result;
}

// Display read results in a formatted table
void displayReadResults(String cardData) {
  Serial.println("\nRead operation completed!");
  Serial.println("+" + String("-").substring(0, 48) + "+");
  
  // Create a clean copy of the data for processing
  String cleanData = cardData;
  cleanData.trim();
  
  if (cardData.length() > 0 && cleanData.length() > 0) {
    Serial.print("| Content:   '");
    Serial.print(cleanData);
    Serial.print("'");
    
    // Pad the line
    int spaces = 30 - cleanData.length();
    for (int i = 0; i < spaces; i++) {
      Serial.print(" ");
    }
    Serial.println(" |");
  } else {
    Serial.println("| Content:   Empty or uninitialized            |");
  }
  
  Serial.println("+" + String("-").substring(0, 48) + "+");
  Serial.println("Read operation completed successfully!");
}

