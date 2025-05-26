import RPi.GPIO as GPIO
import time
from gpt_interpreter import interpret_command
import json
import ast

# Define motor pins (one set shown; extend as needed per motor)
MOTORS = {
    "M0": [17, 18, 27, 22],
    "M1": [5, 6, 13, 19],
    "M2": [12, 16, 20, 21],
    "M3": [23, 24, 25, 8],
    "M4": [7, 1, 0, 11]
}

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
    for pins in MOTORS.values():
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)

def rotate(motor_id, steps, delay=0.002):
    pins = MOTORS.get(motor_id)
    if not pins:
        print(f"Invalid motor ID: {motor_id}")
        return
    for _ in range(steps):
        for step in SEQUENCE:
            for pin, val in zip(pins, step):
                GPIO.output(pin, val)
            time.sleep(delay)

def process_single_command(cmd):
    motor = cmd.get("motor")
    steps = cmd.get("steps", 0)
    rotate(motor, steps)

def process_command(command):
    if isinstance(command, list):
        for cmd in command:
            process_single_command(cmd)
    elif isinstance(command, dict):
        process_single_command(command)

def main():
    setup()
    print("Stepper Worm Control - Type natural language or 'q' to quit.")
    while True:
        nl = input("Command: ")
        if nl.strip().lower() == 'q':
            break
        cmd_str = interpret_command(nl)
        try:
            command = json.loads(cmd_str)
        except:
            command = ast.literal_eval(cmd_str)
        process_command(command)
    GPIO.cleanup()

if __name__ == "__main__":
    main()