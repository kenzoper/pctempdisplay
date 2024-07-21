#include <Arduino.h>

#include "Adafruit_LEDBackpack.h"

Adafruit_7segment gDisplay = Adafruit_7segment();

const uint8_t kBuiltinLed = 13;

void setup()
{
  pinMode(kBuiltinLed, OUTPUT);

  gDisplay.begin(0x70);
  gDisplay.setBrightness(12);
  gDisplay.print("bar");
  gDisplay.writeDisplay();
  delay(5000);
}

void loop()
{

  static int cpuTemp = 0;
  static int gpuTemp = 0;

  if (Serial.available())
  {
    String receivedData = Serial.readStringUntil('\n');
    char system = receivedData[0];

    int temperature = receivedData.substring(2).toInt();

    switch (system)
    {
    case 'C':
      cpuTemp = temperature;
      break;
    case 'G':
      gpuTemp = temperature;
      break;
    default:
      break;
    }
    gDisplay.print(cpuTemp * 100 + gpuTemp);
    gDisplay.writeDigitRaw(2, 0x02);
    gDisplay.writeDisplay();
    delay(1000);
  }
}
