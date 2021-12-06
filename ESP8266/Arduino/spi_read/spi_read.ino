/* 
 ESP 8266 (NodeMCU ESP12E)

A simple SPI to RS284 converter that provides us with some distance capability.

Sketch reads the thermocouple, and sends the following string out on TTL port which goes onto RS485.
|value   |meaning                |
|----    |-----                  |
|0x02    |START-OF-TELEGRAM      |
|'5'     |sensor number (ASCII)  |
|0x09    |END-OF-FIELD           |
|'25.0'  |temperature (ASCII)    |
|0x03    |END-OF-TELEGRAM        |

Notes:
Label GPIO  Input Output  Notes
D0  GPIO16  no interrupt  no PWM or I2C support HIGH at boot
used to wake up from deep sleep
D1  GPIO5 OK  OK  often used as SCL (I2C)
D2  GPIO4 OK  OK  often used as SDA (I2C)
D3  GPIO0 pulled up OK  connected to FLASH button, boot fails if pulled LOW
D4  GPIO2 pulled up OK  HIGH at boot
connected to on-board LED, boot fails if pulled LOW
D5  GPIO14  OK  OK  SPI (SCLK)
D6  GPIO12  OK  OK  SPI (MISO)
D7  GPIO13  OK  OK  SPI (MOSI)
D8  GPIO15  pulled to GND OK  SPI (CS)
Boot fails if pulled HIGH
RX  GPIO3 OK  RX pin  HIGH at boot
TX  GPIO1 TX pin  OK  HIGH at boot
debug output at boot, boot fails if pulled LOW
A0  ADC0  Analog Input  X 

Pins:
             +-ANT--+
      ADC0   +      + GPIO16 WAKE
      RES    +      + GPIO5  SCL
      RES    +      + GPIO4  SDA
SDD3  GPIO10 +      + GPIO0  FLASH
SDD2  GPIO9  +      + GPIO5  TXD1
SDD1  MOSI   +      + 3V3
SDCMD CS     +      + GND
SDD0  MISO   +      + GPIO14 SCLK
SDCLK SCLK   +      + GPIO12 MISO
      GND    +      + GPIO13 MOSI  RXD2
      3V3    +    H + GPIO15 CS    TXD2
      EN     +    S + GPIO3  RXD0
      RST    + T  A + GPIO1  TXD0
      GND    + S  L + GND
      VIN    + R  F + 3V3
             +-USB--+

Next step is to use the loop function in a Modbus RTU slave implementation
https://www.arduino.cc/en/ArduinoModbus/ArduinoModbus
and on the pi
https://minimalmodbus.readthedocs.io/en/master/usage.html
which requires https://minimalmodbus.readthedocs.io/en/master/installation.html

FTDI-RS232 3V3
GND   BLACK
CTS#  BROWN
VCC   RED
TXD   ORANGE
RXD   YELLOW
RTS#  GREEN

RS485 board:

------+
      + ENABLE
      + DI
      + DO
      + GnD
      + 3v3
------+

*/

#include<SPI.h>
#include <ESP8266WiFi.h>

const int slaveAPin = D8;  // chip select
const int rsEnPin = D1;    // RS422 enable
// serial message simple farming
const unsigned char START_TEXT = 0x02;
const unsigned char END_FIELD = 0x09;
const unsigned char END_TEXT = 0x03;
int BAUD_RATE = 9600;

void setup() {
  // put your setup code here, to run once:
  WiFi.mode(WIFI_OFF);
  pinMode (slaveAPin, OUTPUT);
  digitalWrite (slaveAPin, LOW);
  pinMode (rsEnPin, OUTPUT);
  digitalWrite (rsEnPin, LOW);
  SPI.beginTransaction(SPISettings(4000000, MSBFIRST, SPI_MODE0));
  SPI.begin();  /* begin SPI */

  Serial.begin(115200);
  Serial1.begin(BAUD_RATE, SERIAL_8N1);
}

uint16_t rawValue;
float celcius;

// --------------------- ReadMax6675 -----------------------------------------------
float ReadMax6675() {
  // https://www.arduino.cc/en/Reference/SPI
  // MAX6675
  digitalWrite (slaveAPin, LOW);
  delay(1);
  rawValue = SPI.transfer(0);
  rawValue<<=8;
  rawValue |= SPI.transfer(0);
  digitalWrite (slaveAPin, HIGH);
  delay(1);
  Serial.print("SPI DATA[");
  Serial.print(rawValue, HEX);
  Serial.println("]");
  //
  if ((rawValue& 0x04) || (0 == rawValue))
  { 
    Serial.println("NAN/invalid");
    rawValue = SPI.transfer(0);
    Serial.print("EAT DATA[");
    Serial.print(rawValue, HEX);
    Serial.println("]");
    return(-1.0);
  }else {
    rawValue >>=3;  // discard lowest 3 bits (status)
    celcius = rawValue*0.25;
    Serial.print(celcius, 3);
    Serial.println(" celcius");
  
    return(celcius);
  }
}

// -------------------- calc_interval ------------------------------------------------
int calc_interval(int count) {
  return((11* 1000 * count / BAUD_RATE) +1);
}

// -------------------- WriteTelegram ------------------------------------------------
void WriteTelegram(int sensor, float value) {
  char telegram[80];
  int offset=0;
  char buff[20];

  digitalWrite (rsEnPin, HIGH);
  telegram[0] = START_TEXT;
  offset+=1;
  sprintf(buff, "%d", sensor);
  strcpy(&telegram[offset], buff);
  offset+=strlen(buff);
  telegram[offset] = END_FIELD;
  offset+=1;
  sprintf(buff, "%4.3f", value);
  strcpy(&telegram[offset], buff);
  offset+=strlen(buff);
  telegram[offset] = END_TEXT;
  Serial1.write(telegram, offset);
  delay(calc_interval(offset));
  digitalWrite (rsEnPin, LOW);

  offset+=1;
  telegram[offset] = 0;
  Serial.println(telegram);
}

void loop() {
  // put your main code here, to run repeatedly:
  float value = ReadMax6675();

  WriteTelegram(5, value);
  delay(200);
}
