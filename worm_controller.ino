#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm;

// Servo pulse range
#define SERVOMIN 150
#define SERVOMAX 600

// Corrected Channels
#define BR 0
#define FR 1
#define BL 2
#define FL 3
#define MID 4  // Mouth

// Angles
#define SERVO_NEUTRAL       90
#define MOUTH_FULL_OPEN      0
#define MOUTH_CLOSED        180

// Function declarations
void resetAll();
void tiltFrontLeft();
void tiltFrontRight();
void tiltBackLeft();
void tiltBackRight();
void openAndCloseMouth();
void choreographedTalk();
void holdMouthOpen();
void closeMouth();
void testAll();
void dance();
void sadness();
void setAngle(uint8_t ch, int deg);

void setup() {
  Serial.begin(115200);  // Match Python baud rate
  pwm.begin();
  pwm.setPWMFreq(50);
  delay(200);
  randomSeed(analogRead(0));
  resetAll();
  Serial.println("🤖 WORM Arduino Controller Ready!");
  Serial.println("Commands: fl, fr, bl, br, b, t, d, om, cm, choreographedTalk, sadness");
}

void loop() {
  if (!Serial.available()) return;

  String cmd = Serial.readStringUntil('\n');
  cmd.trim();
  Serial.print("Command received: ");
  Serial.println(cmd);

  // Handle Python commands
  if      (cmd == "fl") tiltFrontLeft();
  else if (cmd == "fr") tiltFrontRight();
  else if (cmd == "bl") tiltBackLeft();
  else if (cmd == "br") tiltBackRight();
  else if (cmd == "b")  resetAll();
  else if (cmd == "t")  choreographedTalk();
  else if (cmd == "d")  dance();
  else if (cmd == "om") holdMouthOpen();
  else if (cmd == "cm") closeMouth();
  else if (cmd == "choreographedTalk") choreographedTalk();
  else if (cmd == "sadness") sadness();
  else if (cmd == "ta") testAll();
  else {
    Serial.print("Unknown command: ");
    Serial.println(cmd);
  }
}

void resetAll() {
  setAngle(FL, SERVO_NEUTRAL);
  setAngle(FR, SERVO_NEUTRAL);
  setAngle(BL, SERVO_NEUTRAL);
  setAngle(BR, SERVO_NEUTRAL);
  setAngle(MID, MOUTH_CLOSED);
  Serial.println("Reset → all servos to neutral");
}

void dance() {
  Serial.println("🕺 Dance animation starting...");
  
  tiltFrontRight(); delay(800);
  tiltBackLeft();   delay(800);
  tiltFrontRight(); delay(800);
  tiltBackLeft();   delay(800);
  tiltFrontRight(); delay(500);
  
  resetAll();
  Serial.println("🕺 Dance complete!");
}

void sadness() {
  Serial.println("😢 Sadness movement...");
  
  // Slow, drooping movements
  setAngle(FL, 45);   // Droop front
  setAngle(FR, 45);
  delay(1000);
  
  setAngle(BL, 135);  // Slight back lift
  setAngle(BR, 135);
  delay(1500);
  
  resetAll();
  Serial.println("😢 Sadness complete");
}

void tiltFrontLeft() {
  Serial.println("Tilt front left");
  setAngle(FL, 180);  // pull
  setAngle(BR, 0);    // release
}

void tiltFrontRight() {
  Serial.println("Tilt front right");
  setAngle(FR, 180);  // pull
  setAngle(BL, 0);    // release
}

void tiltBackLeft() {
  Serial.println("Tilt back left");
  setAngle(BL, 180);  // pull
  setAngle(FR, 0);    // release
}

void tiltBackRight() {
  Serial.println("Tilt back right");
  setAngle(BR, 180);  // pull
  setAngle(FL, 0);    // release
}

void openAndCloseMouth() {
  Serial.println("Open and close mouth");
  setAngle(MID, MOUTH_FULL_OPEN);
  delay(600);
  setAngle(MID, MOUTH_CLOSED);
}

void choreographedTalk() {
  Serial.println("🗣️ Choreographed talking...");

  setAngle(MID, MOUTH_FULL_OPEN); delay(200);
  setAngle(MID, MOUTH_CLOSED);    delay(150);

  setAngle(MID, 90);              delay(150); // halfway
  setAngle(MID, MOUTH_CLOSED);    delay(150);

  setAngle(MID, 90);              delay(150); // halfway again
  setAngle(MID, MOUTH_CLOSED);    delay(150);

  setAngle(MID, 135);             delay(120); // quarter open
  setAngle(MID, MOUTH_CLOSED);    delay(150);

  setAngle(MID, MOUTH_FULL_OPEN); delay(220);
  setAngle(MID, MOUTH_CLOSED);    delay(150);
  
  Serial.println("🗣️ Talk animation complete");
}

void holdMouthOpen() {
  Serial.println("Hold mouth open");
  setAngle(MID, MOUTH_FULL_OPEN);
}

void closeMouth() {
  Serial.println("Close mouth");
  setAngle(MID, MOUTH_CLOSED);
}

void testAll() {
  Serial.println("🧪 Testing all movements...");
  
  tiltFrontRight(); delay(800); resetAll(); delay(400);
  tiltFrontLeft();  delay(800); resetAll(); delay(400);
  tiltBackRight();  delay(800); resetAll(); delay(400);
  tiltBackLeft();   delay(800); resetAll(); delay(400);
  holdMouthOpen();  delay(800); closeMouth(); delay(400);
  choreographedTalk();
  dance();
  
  Serial.println("🧪 Test sequence complete!");
}

void setAngle(uint8_t ch, int deg) {
  deg = constrain(deg, 0, 180);
  int pulse = map(deg, 0, 180, SERVOMIN, SERVOMAX);
  pwm.setPWM(ch, 0, pulse);
} 