#include "IR.h"
#define IR_Pin 17

String decodeKeyValue(unsigned long data) {
  switch (data) {
    case 0xFF629D: return "UP";
    case 0xFFA857: return "DOWN";
    case 0xFF22DD: return "LEFT";
    case 0xFFC23D: return "RIGHT";
    case 0xFF02FD: return "OK";
    case 0xFF6897: return "1";
    case 0xFF9867: return "2";
    case 0xFFB04F: return "3";
    case 0xFF30CF: return "4";
    case 0xFF18E7: return "5";
    case 0xFF7A85: return "6";
    case 0xFF10EF: return "7";
    case 0xFF38C7: return "8";
    case 0xFF5AA5: return "9";
    case 0xFF4AB5: return "0";
    case 0xFF42BD: return "*";
    case 0xFF52AD: return "#";
    default: 
      // For debugging: print the received code
      Serial.print("Raw IR Code: 0x");
      Serial.println(data, HEX);
      return "ERROR";
  }
}

void setup() {
  Serial.begin(115200);
  IR_Init(IR_Pin);
}

void loop() {
  if(flagCode) {
    unsigned long irValue = IR_Decode(flagCode);
    if(irValue != 0xFFFFFFFF) {  // Ignore repeat codes
      String keyName = decodeKeyValue(irValue);
      Serial.println(keyName);
    }
    IR_Release();
  }
}