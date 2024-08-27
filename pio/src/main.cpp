#include <Wire.h>
#include <Adafruit_GFX.h>
#include "Adafruit_LEDBackpack.h"
#include <iostream>
#include <cstdint>
#include <Adafruit_DotStar.h>
#include <SPI.h>

#define NUMPIXELS 40  
#define CPU_MIN_TEMP 30
#define CPU_MAX_TEMP 90
#define GPU_MIN_TEMP 25
#define GPU_MAX_TEMP 90

Adafruit_AlphaNum4 alpha4 = Adafruit_AlphaNum4();
Adafruit_DotStar strip(NUMPIXELS, DOTSTAR_BGR);

void setup()
{
    Serial.begin(9600);

    alpha4.begin(0x70);
    alpha4.writeDigitAscii(0, 'b');
    alpha4.writeDigitAscii(1, 'o');
    alpha4.writeDigitAscii(2, 'o');
    alpha4.writeDigitAscii(3, 't');
    alpha4.writeDisplay();

    strip.begin();
    strip.show();
}

void setColor(int index, int color) {
  strip.setPixelColor(index,color);
}

void setLEDs(int startLED, int endLED, int gradientArr[6]) {
  int arrIndex = 0;
  int counter = 0;

  if (startLED < endLED) {
    for (int i = startLED; i < endLED; i++) {
      strip.setPixelColor(i,gradientArr[arrIndex]);
      counter++;
      if (counter % 3 == 0) {
        arrIndex++;
      }
    }
  }

  if (startLED > endLED) {
    for (int i = startLED; i > endLED; i--) {
      strip.setPixelColor(i,gradientArr[arrIndex]);
      counter++;
      if (counter % 3 == 0) {
        arrIndex++;
      }
    }
  }
}

int gradient [6] = {0x0000FF,0x3300CC,0x660099,0x990066,0xCC0033,0xFF0000};

void writeTemperature(uint8_t display, int value)
{
    uint8_t offset = 0;
    if (display > 0)
    {
        offset = 2;
    }
    if (value > 99)
    {
        alpha4.writeDigitAscii(offset, 'H');

        alpha4.writeDigitAscii(offset + 1, 'I');
    }
    else
    {
        alpha4.writeDigitAscii(offset, value / 10 + '0');

        alpha4.writeDigitAscii(offset + 1, value % 10 + '0');
    }
    
}

void loop()
{
    char receivedData;
    if (Serial.available())
    {
        Serial.readBytes(&receivedData, 1);
        uint8_t remaining_bits = receivedData & 0x7F;

        int value = static_cast<int>(remaining_bits);

        uint8_t display = receivedData & 0x80;
        writeTemperature(display, value);

        alpha4.writeDisplay();

        if (display == 0) {
            strip.fill(0,1,18);
            uint8_t grad_value = constrain(value, CPU_MIN_TEMP, CPU_MAX_TEMP);
            setLEDs(1,map(grad_value,CPU_MIN_TEMP,CPU_MAX_TEMP,1,19),gradient);
        } else {
            strip.fill(0,21,18);
            uint8_t grad_value = constrain(value, GPU_MIN_TEMP, GPU_MAX_TEMP);
            setLEDs(39,map(value,GPU_MIN_TEMP,GPU_MAX_TEMP,39,21),gradient);
        }
        strip.show();
        

        strip.setBrightness(25);
        
    }
}
