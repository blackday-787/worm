import json
import time
import serial
import os

# Load port config
SERIAL_PORT = os.getenv("WORM_SERIAL_PORT", "/dev/cu.usbmodem1401")
BAUD_RATE = int(os.getenv("WORM_BAUD_RATE", 9600))
arduino = serial.Serial(SERIAL_PORT, BAUD_RATE)
time.sleep(2)

def send_command_to_serial(output):
    try:
        output = output.strip()

        # If it's one of the symbolic Arduino commands
        if output in ["b", "fl", "fr", "bl", "br", "t", "m1", "om", "cm", "ta", "d"]:
            arduino.write((output + "\n").encode())
            print(f"[SERIAL] → {output}")
            return

        # Otherwise, parse as JSON motor commands
        commands = json.loads(output)
        if isinstance(commands, dict):
            commands = [commands]

        for cmd in commands:
            servo = cmd["servo"]
            angle = cmd["angle"]
            line = f"{servo},{angle}\n"
            arduino.write(line.encode())
            print(f"[SERIAL] → {line.strip()}")
            time.sleep(0.1)

    except Exception as e:
        print("[ERROR] Failed to send command:", e)
