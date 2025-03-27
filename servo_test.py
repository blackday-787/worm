from gpt_interpreter import interpret_command  # Import our GPT-4 command interpreter function
import json
import ast  # For fallback parsing of non-standard JSON outputs
import serial  # For serial communication with Arduino
import time

# Define serial connection parameters
SERIAL_PORT = "/dev/cu.usbmodem2101"
BAUD_RATE = 9600

# Define a default angle for all servos
DEFAULT_ANGLE = 90

# Open serial connection to the Arduino
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Wait a moment for the connection to stabilize

def return_all_servos_to_default():
    """
    Sends a command to each servo channel (0-4) to move to the default position.
    """
    for channel in range(5):  # Assuming servo channels are 0, 1, 2, 3, and 4
        serial_command = f"{channel} {DEFAULT_ANGLE}\n"
        print(f"Returning servo {channel} to default position: {DEFAULT_ANGLE} degrees")
        ser.write(serial_command.encode())
        response = ser.readline().decode().strip()  # Read Arduino's response, if available
        print(f"Arduino says: {response}")
        time.sleep(0.2)  # Small delay between commands

def main():
    # At the very beginning, return all servos to their default positions.
    print("Resetting all servos to default position...")
    return_all_servos_to_default()

    print("Animatronic Worm Controller - Interactive Mode")
    print("Type your natural language command (or 'q' to quit):")

    # Interactive loop for natural language commands.
    while True:
        nl_command = input("Natural language command: ")
        if nl_command.lower() == 'q':
            break

        # Use GPT-4 to interpret the command.
        command_str = interpret_command(nl_command)
        if command_str is None:
            print("Failed to interpret command using GPT-4.")
            continue

        print("Interpreted JSON command:", command_str)
        try:
            # Try parsing the response as JSON.
            command = json.loads(command_str)
        except json.JSONDecodeError:
            try:
                # Fallback: use Python's literal evaluation.
                command = ast.literal_eval(command_str)
            except Exception as e:
                print("Error: Unable to decode GPT-4 response.", e)
                continue

        # Extract values from the command.
        channel = command.get("servo")
        angle = command.get("angle")
        
        # Check if channel is a string.
        if isinstance(channel, str):
            if channel.lower() == "all":
                print("Returning all servos to default position (via command).")
                return_all_servos_to_default()
                continue
            else:
                print("Invalid servo channel value: must be an integer (0-4) or 'all'.")
                continue

        # Convert angle to integer if necessary.
        try:
            angle = int(angle)
        except ValueError:
            print("Invalid angle value: must be an integer.")
            continue

        # Now perform numeric validation.
        if not (0 <= channel <= 4 and 0 <= angle <= 180):
            print("Invalid command values received from GPT-4. Check that servo is 0-4 and angle is 0-180.")
            continue

        # Send the command to the Arduino.
        serial_command = f"{channel} {angle}\n"
        ser.write(serial_command.encode())
        response = ser.readline().decode().strip()
        print(f"Arduino says: {response}")

    # Close the serial connection when exiting the loop.
    ser.close()
    print("Serial connection closed. Exiting.")

if __name__ == "__main__":
    main()
