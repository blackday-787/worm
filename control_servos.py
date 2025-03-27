import serial
import time

# Define serial connection
SERIAL_PORT = "/dev/cu.usbmodem2101"
BAUD_RATE = 9600

# Open serial connection
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Wait for the connection to stabilize

# Move servos in sequence (you can modify this logic)
for channel in range(5):  # Servo channels 0-4
    ser.write(f"{channel} 90\n".encode())  # Move servo to 90°
    time.sleep(1)  # Wait for movement to complete

# Close serial connection
ser.close()
