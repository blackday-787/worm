import RPi.GPIO as GPIO
import time

PINS = [17, 18, 27, 22]
SEQUENCE = [
    [1, 0, 0, 1],
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
]

def setup():
    GPIO.setmode(GPIO.BCM)
    for pin in PINS:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)

def rotate(steps):
    for _ in range(steps):
        for step in SEQUENCE:
            for pin, val in zip(PINS, step):
                GPIO.output(pin, val)
            time.sleep(0.002)

setup()
rotate(1024)  # ~180° test
GPIO.cleanup()
