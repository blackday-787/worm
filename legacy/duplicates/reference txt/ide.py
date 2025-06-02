#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

// Function prototypes
void moveServo(int servoChannel, int angle);
void stop_servos();

#define SERVO_MIN 150  // Pulse for 0° position
#define SERVO_MAX 600  // Pulse for 180° position
#define SERVO_90 ((SERVO_MIN + SERVO_MAX) / 2)  // Pulse for 90° position

void setup() {
  pwm.begin();
  pwm.setPWMFreq(60); // Set frequency to 60 Hz (typical for servos)
  delay(10);

  // Initialize all 5 servos to default (0°) position
  for (uint8_t channel = 0; channel < 5; channel++) {
    pwm.setPWM(channel, 0, SERVO_MIN);
  }

  Serial.begin(9600);
  delay(100);  // Wait for Serial to stabilize
  
  // Flush any leftover characters from the serial buffer
  while (Serial.available() > 0) {
    Serial.read();
  }
  
  Serial.println("Arduino Ready!");
}

void moveServo(int servoChannel, int angle) {
  if (servoChannel < 0 || servoChannel > 4) {
    Serial.println("Invalid Servo Channel");
    return;
  }
  if (angle < 0 || angle > 180) {
    Serial.println("Invalid Angle");
    return;
  }

  int pulseLength = map(angle, 0, 180, SERVO_MIN, SERVO_MAX);
  pwm.setPWM(servoChannel, 0, pulseLength);

  Serial.print("Servo ");
  Serial.print(servoChannel);
  Serial.print(" moved to ");
  Serial.print(angle);
  Serial.println(" degrees");
}

void stop_servos() {
  for (uint8_t channel = 0; channel < 5; channel++) {
    pwm.setPWM(channel, 0, 0);  // Stop the servo (set to neutral pulse, no movement)
    delay(0);  // Brief delay per servo
  }
  Serial.println("All servos stopped.");
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');  // Read incoming serial data until newline
    input.trim();
    
    // Debug: Print the raw command received
    Serial.print("Received command: ");
    Serial.println(input);

    int servoChannel, angle;
    if (sscanf(input.c_str(), "%d %d", &servoChannel, &angle) == 2) {
      moveServo(servoChannel, angle);
    } else if (input == "stop") {
      stop_servos();
    } else {
      Serial.println("Invalid command format. Use: [servo] [angle] or 'stop'");
    }
    
    delay(50); // Short delay after processing a command

    // Flush the serial input buffer after processing
    while (Serial.available() > 0) {
      Serial.read();
    }
  }
}
