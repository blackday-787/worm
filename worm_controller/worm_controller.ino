#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm;

// Servo pulse range
#define SERVOMIN 150
#define SERVOMAX 600

// Servo Channels
#define BR 0
#define FR 1
#define BL 2
#define FL 3
#define MID 4  // Mouth
#define SR 5   // Side Right (wiggle)
#define SL 6   // Side Left (wiggle)

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
void testAll();
void testServoOrder();
void dance();
void wiggleRight();
void wiggleLeft();
void wiggleBoth();
void wiggleContinuous();
void setAngle(uint8_t ch, int deg);

void setup() {
  Serial.begin(115200);
  pwm.begin();
  pwm.setPWMFreq(50);
  delay(100);
  randomSeed(analogRead(0));
  resetAll();
  Serial.println("WORM Ready");
  Serial.println("Commands: fl,fr,bl,br,b,d,sr,sl,w,om,cm,ta,identify");
}

void loop() {
  if (!Serial.available()) return;

  String cmd = Serial.readStringUntil('\n');
  cmd.trim();
  Serial.print("Command received: ");
  Serial.println(cmd);

  if      (cmd == "fl") tiltFrontLeft();
  else if (cmd == "fr") tiltFrontRight();
  else if (cmd == "bl") tiltBackLeft();
  else if (cmd == "br") tiltBackRight();
  else if (cmd == "b")  resetAll();
  else if (cmd == "d")  dance();
  else if (cmd == "sr") wiggleRight();
  else if (cmd == "sl") wiggleLeft();
  else if (cmd == "wb") wiggleBoth();
  else if (cmd == "w")  wiggleContinuous();
  else if (cmd == "om") openAndCloseMouth();
  else if (cmd == "cm") setAngle(MID, MOUTH_CLOSED);
  else if (cmd == "ta") testAll();
  else if (cmd == "identify") testServoOrder();
  else if (cmd == "tsr") { Serial.println("Testing SR only"); setAngle(SR, 180); delay(1000); setAngle(SR, 0); delay(1000); setAngle(SR, 90); }
  else if (cmd == "tsl") { Serial.println("Testing SL only"); setAngle(SL, 180); delay(1000); setAngle(SL, 0); delay(1000); setAngle(SL, 90); }
  else if (cmd == "tboth") { Serial.println("Testing both simultaneously"); setAngle(SR, 180); setAngle(SL, 0); delay(2000); setAngle(SR, 0); setAngle(SL, 180); delay(2000); setAngle(SR, 90); setAngle(SL, 90); }
  else if (cmd == "diag") { 
    Serial.println("Hardware diagnostic...");
    Serial.println("Testing PWM channels 5 and 6");
    for(int i = 0; i <= 180; i += 30) {
      Serial.print("Setting both to "); Serial.println(i);
      setAngle(SR, i); 
      delay(500);  // Stagger the commands
      setAngle(SL, i);
      delay(1500);
    }
    resetAll();
  }
  else if (cmd == "ch5") { Serial.println("Testing channel 5 (SR)"); setAngle(5, 0); delay(1000); setAngle(5, 180); delay(1000); setAngle(5, 90); }
  else if (cmd == "ch6") { Serial.println("Testing channel 6 (SL)"); setAngle(6, 0); delay(1000); setAngle(6, 180); delay(1000); setAngle(6, 90); }
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
  setAngle(SR, SERVO_NEUTRAL);
  setAngle(SL, SERVO_NEUTRAL);
  Serial.println("Reset to neutral (SR/SL = 90)");
}

void dance() {
  Serial.println("Dance");
  tiltFrontRight(); delay(800);
  tiltBackLeft();   delay(800);
  tiltFrontRight(); delay(800);
  tiltBackLeft();   delay(800);
  tiltFrontRight(); delay(500);
  resetAll();
}

void tiltFrontLeft() {
  Serial.println("Tilt front left");
  setAngle(FL, 180);
  setAngle(BR, 0);
}

void tiltFrontRight() {
  Serial.println("Tilt front right");
  setAngle(FR, 180);
  setAngle(BL, 0);
}

void tiltBackLeft() {
  Serial.println("Tilt back left");
  setAngle(BL, 180);
  setAngle(FR, 0);
}

void tiltBackRight() {
  Serial.println("Tilt back right");
  setAngle(BR, 180);
  setAngle(FL, 0);
}

void openAndCloseMouth() {
  Serial.println("Mouth movement");
  setAngle(MID, MOUTH_FULL_OPEN);
  delay(600);
  setAngle(MID, MOUTH_CLOSED);
}

void wiggleRight() {
  Serial.println("Wiggle right: SR tighten (180°), SL release (0°)");
  // Counteracting movement - SR pulls while SL releases
  setAngle(SR, 180);           // SR tightens (pull)
  setAngle(SL, 0);             // SL releases (loose) - counteracts SR
}

void wiggleLeft() {
  Serial.println("Wiggle left: SL tighten (180°), SR release (0°)");
  // Counteracting movement - SL pulls while SR releases  
  setAngle(SL, 180);           // SL tightens (pull)
  setAngle(SR, 0);             // SR releases (loose) - counteracts SL
}

void wiggleBoth() {
  Serial.println("Wiggle both: SR and SL both tighten (180°)");
  setAngle(SR, 180);           // Both servos pull
  setAngle(SL, 180);           // simultaneously
}

void wiggleContinuous() {
  Serial.println("Wiggle: SR/SL counteracting");
  
  setAngle(SR, SERVO_NEUTRAL);
  setAngle(SL, SERVO_NEUTRAL);
  delay(200);
  
  for(int i = 0; i < 6; i++) {
    if (i % 2 == 0) {
      Serial.print("W"); Serial.print(i+1); Serial.println(": SR180,SL0");
      setAngle(SR, 180);
      setAngle(SL, 0);
    } else {
      Serial.print("W"); Serial.print(i+1); Serial.println(": SL180,SR0");
      setAngle(SL, 180);
      setAngle(SR, 0);
    }
    delay(300);
  }
  
  Serial.println("Return neutral");
  setAngle(SR, SERVO_NEUTRAL);
  setAngle(SL, SERVO_NEUTRAL);
  delay(200);
}

void testAll() {
  Serial.println("🧪 Testing movements...");
  tiltFrontRight(); delay(800); resetAll(); delay(400);
  tiltFrontLeft();  delay(800); resetAll(); delay(400);
  tiltBackRight();  delay(800); resetAll(); delay(400);
  tiltBackLeft();   delay(800); resetAll(); delay(400);
  openAndCloseMouth(); delay(400);
  
  // Test side servos individually first
  Serial.println("Testing SR servo alone...");
  setAngle(SR, 180); delay(1000);
  setAngle(SR, 90); delay(1000);
  setAngle(SR, 0); delay(1000);
  setAngle(SR, 90); delay(500);
  
  Serial.println("Testing SL servo alone...");
  setAngle(SL, 180); delay(1000);
  setAngle(SL, 90); delay(1000);
  setAngle(SL, 0); delay(1000);
  setAngle(SL, 90); delay(500);
  
  Serial.println("Testing both servos together...");
  wiggleRight(); delay(600);
  wiggleLeft(); delay(600);
  resetAll();
}

void testServoOrder() {
  Serial.println("SERVO ID TEST");
  Serial.println("One servo at a time. Press Enter to continue.");
  
  resetAll();
  delay(500);
  
  for(int ch = 0; ch <= 6; ch++) {
    Serial.print("TEST CH ");
    Serial.println(ch);
    Serial.println("Press Enter...");
    
    while (!Serial.available()) {
      delay(10);
    }
    Serial.readStringUntil('\n');
    
    Serial.print("MOVING CH ");
    Serial.println(ch);
    setAngle(ch, 180);
    
    Serial.println("Which servo moved? Press Enter...");
    while (!Serial.available()) {
      delay(10);
    }
    Serial.readStringUntil('\n');
    
    setAngle(ch, 90);
    Serial.print("CH ");
    Serial.print(ch);
    Serial.println(" done");
  }
  
  Serial.println("TEST COMPLETE");
  resetAll();
}

void setAngle(uint8_t ch, int deg) {
  deg = constrain(deg, 0, 180);
  int pulse = map(deg, 0, 180, SERVOMIN, SERVOMAX);
  pwm.setPWM(ch, 0, pulse);
  Serial.print("DEBUG: Channel ");
  Serial.print(ch);
  Serial.print(" set to ");
  Serial.print(deg);
  Serial.println(" degrees");
}