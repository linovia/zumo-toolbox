#include <ZumoMotors.h>

// I/O Zumo
// Yellow LED: digital pin #13
// User pushbutton: digital pin #12
// Motor driver:
//  - right motor direction: digital pin #7
//  - left motor direction: digital pin #8
//  - right motor speed (PWM): digital pin #9
//  - left motor speed (PWM): digital pin #10
// Buzzer:
//   - digital pin #3 (Arduino Uno or an older Arduino)
//   - digital pin #6 (Arduino Leonardo or A-Star 32U4 Prime)
// Compass / Gyro (Arduino UNO)
//   - SCL (I2C clock) analog pin #5
//   - SDA (I2C data) analog pin #4

#define LED_PIN 13

ZumoMotors motors;

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
}


void loop() {
  char inputBuffer[8];
  int speed;

  if(Serial.available() >= 4) {
    Serial.readBytes(inputBuffer, 4);
    
    // Bits:
    // 0x01: Ping
    // 0X02: LED
    // 0x04: Left motor
    // 0x08: Right motor
    // 0x0C: Both motors
    switch(inputBuffer[0]) {
      case 0x01:
        Serial.write(inputBuffer[1]);
        break;
      case 0x02:
        if (inputBuffer[1] == 1) {
          digitalWrite(LED_PIN, HIGH);
        } else {
          digitalWrite(LED_PIN, LOW);
        }
        break;
      case 0x04:
        speed = (inputBuffer[1]) + (inputBuffer[2] << 8);
        motors.setLeftSpeed(speed);
        Serial.write(inputBuffer[1]);
        Serial.write(inputBuffer[2]);
        Serial.write(highByte(speed));
        Serial.write(lowByte(speed));
        break;
      case 0x08:
        speed = (inputBuffer[1] << 8) + inputBuffer[2];
        motors.setRightSpeed(speed);
        break;
      case 0x0C:
        speed = (inputBuffer[1] << 8) + inputBuffer[2];
        motors.setSpeeds(speed, speed);
        break;
    }
  }
}

