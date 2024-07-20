#include <Arduino.h>

#include "Adafruit_LEDBackpack.h"

Adafruit_7segment gDisplay = Adafruit_7segment();

const uint8_t kBuiltinLed = 13;

void setup() {
  pinMode(kBuiltinLed, OUTPUT);

  gDisplay.begin(0x70);
  gDisplay.setBrightness(12);
  gDisplay.print("foo");
  gDisplay.writeDisplay();
  delay(2000);
}

void loop() {

  if (Serial.available()) {
    String receivedData = Serial.readStringUntil('\n');
    float temperature = receivedData.toFloat();

    gDisplay.print(temperature);
    gDisplay.writeDisplay();
    delay(1000);
  }

}
