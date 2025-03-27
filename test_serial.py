import serial
import time

# Define serial connection
SERIAL_PORT = "/dev/cu.usbmodem2101"
BAUD_RATE = 9600

# Open serial connection
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Allow the connection to stabilize

# Allow user to enter servo channel and angle
while True:
    user_input = input("Enter servo channel (0-4) and angle (0-180), or 'q' to quit: ")
    
    if user_input.lower() == 'q':
        break

    try:
        servo_channel, angle = map(int, user_input.split())
        if 0 <= servo_channel <= 4 and 0 <= angle <= 180:
            command = f"{servo_channel} {angle}\n"
            ser.write(command.encode())  # Send command to Arduino
            response = ser.readline().decode().strip()  # Read response
            print(f"Arduino says: {response}")
        else:
            print("Invalid input. Servo must be 0-4, and angle 0-180.")
    except ValueError:
        print("Invalid format. Use: [servo] [angle] (e.g., '2 90')")

# Close the serial connection
ser.close()
