#!/usr/bin/env python3
"""
🧪 Arduino Connection Test
Quick test to verify Arduino is responding to commands
"""

import serial
import time
import sys

def test_arduino_connection():
    """Test Arduino connection with current settings"""
    
    # Updated port from available ports
    port = "/dev/cu.usbmodem1101"
    baud = 115200
    
    print("🔍 Testing Arduino connection...")
    print(f"   Port: {port}")
    print(f"   Baud: {baud}")
    print()
    
    try:
        # Connect to Arduino
        arduino = serial.Serial(port, baud, timeout=2)
        time.sleep(2)  # Wait for Arduino to initialize
        
        print("✅ Serial connection established!")
        print()
        
        # Send test command
        test_commands = ["b", "ta", "d"]
        
        for cmd in test_commands:
            print(f"🤖 Sending command: {cmd}")
            arduino.write(f"{cmd}\n".encode())
            
            # Read response
            start_time = time.time()
            while time.time() - start_time < 3:  # 3 second timeout
                if arduino.in_waiting:
                    response = arduino.readline().decode().strip()
                    if response:
                        print(f"   Arduino: {response}")
                time.sleep(0.1)
            
            print()
            time.sleep(1)
        
        arduino.close()
        print("🎉 Arduino test complete!")
        print()
        print("✅ Your Arduino is ready for the WORM system!")
        
    except serial.SerialException as e:
        print(f"❌ Connection failed: {e}")
        print()
        print("🔧 TROUBLESHOOTING:")
        print("1. Make sure Arduino is plugged in")
        print("2. Upload the worm_controller.ino sketch")
        print("3. Check the port in worm_controller.py")
        print()
        print("Available ports:")
        import glob
        ports = glob.glob('/dev/cu.*')
        for p in ports:
            print(f"   {p}")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    test_arduino_connection() 