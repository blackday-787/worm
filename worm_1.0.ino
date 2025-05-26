#include <Stepper.h>

#define STEPS_PER_REV 2048
#define STEP_3_5_HALF_REV 614  // ~108° = 3/5 of a half rotation

// Red stepper on pins 8, 9, 10, 11 (ULN2003 input order)
Stepper redStepper(STEPS_PER_REV, 8, 10, 9, 11);

// Green stepper on pins 50, 51, 52, 53 (ULN2003 input order)
Stepper greenStepper(STEPS_PER_REV, 50, 52, 51, 53);

void setup() {
  redStepper.setSpeed(10);     // RPM
  greenStepper.setSpeed(10);   // RPM

  Serial.begin(9600);
  Serial.println("Red CW / Green CCW startup...");
}

void loop() {
  Serial.println("→ Red CW / ← Green CCW");
  redStepper.step(STEP_3_5_HALF_REV);      // Red: clockwise
  greenStepper.step(-STEP_3_5_HALF_REV);   // Green: counter-clockwise

  delay(1000);

  Serial.println("← Red CCW / → Green CW");
  redStepper.step(-STEP_3_5_HALF_REV);     // Red: counter-clockwise
  greenStepper.step(STEP_3_5_HALF_REV);    // Green: clockwise

  delay(2000);
}