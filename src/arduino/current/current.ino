#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVOMIN  150
#define SERVOMAX  600

// Servo channels
#define FL 0  // Front Left
#define FR 1  // Front Right  
#define BL 2  // Back Left
#define BR 3  // Back Right
#define MO 4  // Mouth

// Servo positions
#define SERVO_NEUTRAL    90
#define SERVO_MIN        0
#define SERVO_MAX        180
#define MOUTH_CLOSED     180
#define MOUTH_OPEN       90
#define MOUTH_FULL_OPEN  60  // Added for new talk function

void setup() {
  Serial.begin(115200);
  pwm.begin();
  pwm.setPWMFreq(60);
  delay(100);
  resetAll();
  Serial.println("Ready");
}

void loop() {
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    handleCommand(cmd);
  }
}

void handleCommand(String cmd) {
  if (cmd == "b") {
    resetAll();
    Serial.println("Reset");
  }
  else if (cmd == "d") {
    dance();
    Serial.println("Dance complete");
  }
  else if (cmd == "t") {
    talk();
    Serial.println("Talk complete");
  }
  else if (cmd == "om") {
    setAngle(MO, MOUTH_OPEN);
    Serial.println("Mouth open");
  }
  else if (cmd == "cm") {
    setAngle(MO, MOUTH_CLOSED);
    Serial.println("Mouth closed");
  }
  else if (cmd == "choreographedTalk") {
    choreographedTalk();
    Serial.println("Choreographed talk complete");
  }
  else if (cmd == "fl") {
    tiltFrontLeft();
    Serial.println("Front left");
  }
  else if (cmd == "fr") {
    tiltFrontRight();
    Serial.println("Front right");
  }
  else if (cmd == "bl") {
    tiltBackLeft();
    Serial.println("Back left");
  }
  else if (cmd == "br") {
    tiltBackRight();
    Serial.println("Back right");
  }
  // Custom category movements
  else if (cmd == "encouragement") {
    encouragementMovement();
    Serial.println("Encouragement complete");
  }
  else if (cmd == "excitement") {
    excitementMovement();
    Serial.println("Excitement complete");
  }
  else if (cmd == "curiosity") {
    curiosityMovement();
    Serial.println("Curiosity complete");
  }
  else if (cmd == "relaxation") {
    relaxationMovement();
    Serial.println("Relaxation complete");
  }
  else if (cmd == "celebration") {
    celebrationMovement();
    Serial.println("Celebration complete");
  }
  else if (cmd == "compliments") {
    complimentsMovement();
    Serial.println("Compliments complete");
  }
  else if (cmd == "jokes") {
    jokesMovement();
    Serial.println("Jokes complete");
  }
  else if (cmd == "short_responses") {
    shortResponseMovement();
    Serial.println("Short response complete");
  }
  else {
    Serial.println("Unknown command");
  }
}

void setAngle(int ch, int angle) {
  angle = constrain(angle, SERVO_MIN, SERVO_MAX);
  int pulse = map(angle, 0, 180, SERVOMIN, SERVOMAX);
  pwm.setPWM(ch, 0, pulse);
  delay(20);
}

void moveMouth(int angle) {
  setAngle(MO, angle);
}

void resetAll() {
  setAngle(FL, SERVO_NEUTRAL);
  setAngle(FR, SERVO_NEUTRAL);
  setAngle(BL, SERVO_NEUTRAL);
  setAngle(BR, SERVO_NEUTRAL);
  setAngle(MO, MOUTH_CLOSED);
}

void talk() {
  moveMouth(MOUTH_FULL_OPEN);
  delay(200);
  moveMouth(MOUTH_CLOSED);
  delay(150);
  
  moveMouth(60); // medium open
  delay(150);
  moveMouth(MOUTH_CLOSED);
  delay(100);
  
  moveMouth(45); // small open
  delay(120);
  moveMouth(MOUTH_CLOSED);
  delay(80);
  
  moveMouth(70); // medium-big
  delay(180);
  moveMouth(MOUTH_CLOSED);
  delay(120);
}

void choreographedTalk() {
  // Longer mouth movements for "hello there tate" - about 1.5x longer than regular talk
  setAngle(MO, 160); delay(100);
  setAngle(MO, MOUTH_CLOSED); delay(80);
  setAngle(MO, 135); delay(120);
  setAngle(MO, MOUTH_CLOSED); delay(80);
  setAngle(MO, MOUTH_OPEN); delay(150);
  setAngle(MO, MOUTH_CLOSED); delay(80);
  setAngle(MO, 160); delay(100);
  setAngle(MO, MOUTH_CLOSED);
}

void tiltFrontLeft() {
  setAngle(FL, SERVO_MAX);
  setAngle(BR, SERVO_MIN);
}

void tiltFrontRight() {
  setAngle(FR, SERVO_MAX);
  setAngle(BL, SERVO_MIN);
}

void tiltBackLeft() {
  setAngle(BL, SERVO_MAX);
  setAngle(FR, SERVO_MIN);
}

void tiltBackRight() {
  setAngle(BR, SERVO_MAX);
  setAngle(FL, SERVO_MIN);
}

void dance() {
  for(int i = 0; i < 3; i++) {
    tiltFrontRight();
    setAngle(MO, MOUTH_OPEN);
    delay(300);
    
    tiltBackLeft();
    setAngle(MO, MOUTH_CLOSED);
    delay(300);
  }
  resetAll();
}

// Custom category movement functions

void encouragementMovement() {
  // Gentle forward-backward rocking motion with supportive mouth movements
  setAngle(MO, MOUTH_OPEN);
  
  // Gentle forward lean (encouraging lean-in)
  setAngle(FL, 120); setAngle(FR, 120);
  setAngle(BL, 60); setAngle(BR, 60);
  delay(400);
  
  // Supportive nod back
  setAngle(FL, 60); setAngle(FR, 60);  
  setAngle(BL, 120); setAngle(BR, 120);
  setAngle(MO, MOUTH_CLOSED);
  delay(300);
  
  // Another encouraging lean
  setAngle(FL, 120); setAngle(FR, 120);
  setAngle(BL, 60); setAngle(BR, 60);
  setAngle(MO, 70);
  delay(350);
  
  resetAll();
}

void excitementMovement() {
  // Quick energetic side-to-side wiggles with animated mouth
  setAngle(MO, MOUTH_FULL_OPEN);
  
  for(int i = 0; i < 4; i++) {
    // Quick left wiggle
    setAngle(FL, 45); setAngle(BL, 135);
    setAngle(FR, 135); setAngle(BR, 45);
    delay(150);
    
    // Quick right wiggle  
    setAngle(FL, 135); setAngle(BL, 45);
    setAngle(FR, 45); setAngle(BR, 135);
    delay(150);
    
    // Mouth animation during movement
    if(i % 2 == 0) setAngle(MO, MOUTH_CLOSED);
    else setAngle(MO, MOUTH_FULL_OPEN);
  }
  
  resetAll();
}

void curiosityMovement() {
  // Slow inquisitive head tilts and gentle swaying
  setAngle(MO, 60);
  
  // Curious tilt left
  setAngle(FL, 45); setAngle(BL, 45);
  setAngle(FR, 135); setAngle(BR, 135);
  delay(500);
  
  // Ponder moment
  setAngle(MO, MOUTH_CLOSED);
  delay(200);
  
  // Curious tilt right
  setAngle(FL, 135); setAngle(BL, 135);
  setAngle(FR, 45); setAngle(BR, 45);
  setAngle(MO, 70);
  delay(500);
  
  // Thoughtful pause
  setAngle(FL, 90); setAngle(FR, 90);
  setAngle(BL, 90); setAngle(BR, 90);
  setAngle(MO, MOUTH_CLOSED);
  delay(300);
  
  resetAll();
}

void relaxationMovement() {
  // Slow, flowing wave-like motion - very gentle
  setAngle(MO, 60);
  
  // Slow wave front to back
  setAngle(FL, 60); setAngle(FR, 60);
  delay(600);
  
  setAngle(BL, 120); setAngle(BR, 120);
  setAngle(FL, 120); setAngle(FR, 120);
  delay(600);
  
  // Gentle mouth movement
  setAngle(MO, MOUTH_CLOSED);
  delay(400);
  
  // Return wave
  setAngle(FL, 60); setAngle(FR, 60);
  setAngle(BL, 60); setAngle(BR, 60);
  delay(600);
  
  resetAll();
}

void celebrationMovement() {
  // Enthusiastic full-body celebration with mouth wide open
  setAngle(MO, MOUTH_FULL_OPEN);
  
  // Victory lift (all servos up)
  setAngle(FL, 45); setAngle(FR, 45);
  setAngle(BL, 135); setAngle(BR, 135);
  delay(400);
  
  // Celebration shimmy
  for(int i = 0; i < 3; i++) {
    setAngle(FL, 135); setAngle(BR, 45);
    setAngle(FR, 45); setAngle(BL, 135);
    delay(200);
    
    setAngle(FL, 45); setAngle(BR, 135);
    setAngle(FR, 135); setAngle(BL, 45);
    delay(200);
  }
  
  // Final flourish
  setAngle(FL, 30); setAngle(FR, 30);
  setAngle(BL, 150); setAngle(BR, 150);
  setAngle(MO, MOUTH_CLOSED);
  delay(300);
  
  resetAll();
}

void complimentsMovement() {
  // Gentle, humble swaying with shy mouth movements
  setAngle(MO, 70);
  
  // Modest side sway left
  setAngle(FL, 60); setAngle(BL, 60);
  setAngle(FR, 120); setAngle(BR, 120);
  delay(400);
  
  // Shy mouth close
  setAngle(MO, MOUTH_CLOSED);
  delay(200);
  
  // Gentle sway right
  setAngle(FL, 120); setAngle(BL, 120);
  setAngle(FR, 60); setAngle(BR, 60);
  setAngle(MO, 60);
  delay(400);
  
  // Gracious nod
  setAngle(FL, 60); setAngle(FR, 60);
  setAngle(BL, 120); setAngle(BR, 120);
  delay(300);
  
  resetAll();
}

void jokesMovement() {
  // Playful bouncing motion with chuckling mouth
  setAngle(MO, MOUTH_OPEN);
  
  // Setup pause
  delay(200);
  
  // Bounce for delivery
  for(int i = 0; i < 2; i++) {
    setAngle(FL, 120); setAngle(FR, 120);
    setAngle(BL, 60); setAngle(BR, 60);
    delay(250);
    
    setAngle(FL, 60); setAngle(FR, 60);
    setAngle(BL, 120); setAngle(BR, 120);
    setAngle(MO, MOUTH_CLOSED);
    delay(200);
    setAngle(MO, MOUTH_OPEN);
  }
  
  // Punchline wiggle
  setAngle(FL, 45); setAngle(BR, 45);
  setAngle(FR, 135); setAngle(BL, 135);
  setAngle(MO, MOUTH_FULL_OPEN);
  delay(300);
  
  resetAll();
}

void shortResponseMovement() {
  // Quick, simple acknowledgment gesture
  setAngle(MO, MOUTH_OPEN);
  
  // Quick forward nod
  setAngle(FL, 120); setAngle(FR, 120);
  setAngle(BL, 60); setAngle(BR, 60);
  delay(200);
  
  // Return to neutral
  setAngle(FL, 90); setAngle(FR, 90);
  setAngle(BL, 90); setAngle(BR, 90);
  setAngle(MO, MOUTH_CLOSED);
  delay(150);
  
  resetAll();
} 