"""
🤖 WORM HARDWARE CONTROLLER
Pure hardware control - no AI dependencies
Handles Arduino communication and servo movements
"""

import serial
import time
import os
import glob
import subprocess
from typing import Optional, Dict, Any

class WormController:
    """Pure hardware controller for the worm robot"""
    
    def __init__(self, port: str = None, baud_rate: int = 115200):
        """Initialize Arduino connection with auto-detection"""
        self.port = port
        self.baud_rate = baud_rate
        self.serial_connection = None
        self.connected = False
        self.simulation_mode = False
        
        # Try to connect first and test if Arduino already has the right code
        self.connect()
        
        # Only upload if Arduino doesn't have the wiggle functionality
        if self.connected and not self.test_arduino_functionality():
            print("🔧 Arduino needs updated code, uploading...")
            self.close()  # Close connection for upload
            self.auto_upload_arduino()
            self.connect()  # Reconnect after upload
        elif self.connected:
            print("✅ Arduino already has correct code, skipping upload")
        
    def auto_upload_arduino(self):
        """Automatically upload Arduino sketch if arduino-cli is available"""
        try:
            # Check if arduino-cli is installed
            result = subprocess.run(['arduino-cli', 'version'], 
                                  capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                print("🔧 Arduino CLI detected, checking if upload is needed...")
                
                # Find Arduino port for upload
                upload_port = self.find_arduino_port()
                if not upload_port:
                    print("No Arduino port found for upload")
                    return
                
                # Upload command
                sketch_path = "worm_controller/worm_controller.ino"
                if os.path.exists(sketch_path):
                    # Try different board types
                    board_types = [
                        'arduino:avr:uno',       # Arduino Uno (try first)
                        'arduino:avr:nano',      # Arduino Nano
                        'arduino:avr:mega'       # Arduino Mega (last)
                    ]
                    
                    for board in board_types:
                        try:
                            print(f"📡 Uploading {sketch_path} to {upload_port} (board: {board})...")
                            upload_cmd = [
                                'arduino-cli', 'compile', '--upload',
                                '-p', upload_port,
                                '-b', board,
                                sketch_path
                            ]
                            
                            result = subprocess.run(upload_cmd, capture_output=True, text=True, timeout=45)
                            
                            if result.returncode == 0:
                                print("✅ Arduino code uploaded successfully!")
                                print("⏳ Waiting for Arduino to restart...")
                                time.sleep(4)  # Extra time for restart
                                return True
                            else:
                                print(f"⚠️  Upload failed with {board}, trying next board type...")
                                continue
                                
                        except subprocess.TimeoutExpired:
                            print(f"⚠️  Upload timed out with {board}, trying next...")
                            continue
                    
                    print("❌ Upload failed with all board types")
                    print("💡 Try uploading manually through Arduino IDE")
                else:
                    print("Arduino sketch file not found")
            else:
                print("Arduino CLI not properly installed")
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("Arduino CLI not available, skipping auto-upload")
            print("💡 Install arduino-cli for automatic code uploads")
        except Exception as e:
            print(f"Auto-upload error: {e}")
            print("💡 You can upload manually through Arduino IDE")
    
    def find_arduino_port(self):
        """Auto-detect Arduino port"""
        # Common Arduino port patterns
        port_patterns = [
            '/dev/cu.usbmodem*',
            '/dev/ttyUSB*',
            '/dev/ttyACM*'
        ]
        
        possible_ports = []
        for pattern in port_patterns:
            possible_ports.extend(glob.glob(pattern))
        
        # Filter out debug/bluetooth ports
        filtered_ports = [p for p in possible_ports if 'debug' not in p.lower() and 'bluetooth' not in p.lower()]
        
        if filtered_ports:
            print(f"Auto-detected Arduino ports: {filtered_ports}")
            return filtered_ports[0]  # Return first valid port
        
        return None
        
    def connect(self):
        """Connect to the Arduino with auto-detection"""
        # If no port specified, try to auto-detect
        if not self.port:
            self.port = self.find_arduino_port()
            
        if not self.port:
            print("No Arduino port found - running in simulation mode")
            self.connected = False
            self.simulation_mode = True
            return
            
        try:
            self.serial_connection = serial.Serial(self.port, self.baud_rate, timeout=0.5)
            time.sleep(1)  # Reduced from 2 seconds to 1 second
            self.connected = True
            print(f"✅ Arduino connected on {self.port}")
        except Exception as e:
            print(f"⚠️  Arduino connection failed on {self.port}: {e}")
            print("🤖 Running in simulation mode")
            self.connected = False
            self.simulation_mode = True
    
    def send_command(self, command: str) -> bool:
        """Send command to Arduino and return success status"""
        if not self.connected:
            print(f"🤖 [SIMULATION] Arduino command: {command}")
            return True
            
        try:
            self.serial_connection.write(f"{command}\n".encode())
            print(f"🤖 Sent to Arduino: {command}")
            
            # Read Arduino response if available
            time.sleep(0.1)
            if self.serial_connection.in_waiting:
                try:
                    response = self.serial_connection.readline().decode('utf-8', errors='ignore').strip()
                    if response:
                        print(f"🤖 Arduino: {response}")
                except UnicodeDecodeError:
                    # Handle any encoding issues gracefully
                    response = self.serial_connection.readline().decode('ascii', errors='ignore').strip()
                    if response:
                        print(f"🤖 Arduino: {response}")
                
            return True
        except Exception as e:
            print(f"❌ Serial communication error: {e}")
            return False
    
    def move_forward_left(self):
        """Move forward and tilt left"""
        return self.send_command("fl")
    
    def move_forward_right(self):
        """Move forward and tilt right"""
        return self.send_command("fr")
    
    def move_back_left(self):
        """Move back and tilt left"""
        return self.send_command("bl")
    
    def move_back_right(self):
        """Move back and tilt right"""
        return self.send_command("br")
    
    def test_servo_order(self):
        """Test servo order for identification"""
        return self.send_command("identify")
    
    def side_left(self):
        """Side tendon left (channel 5)"""
        return self.send_command("sl")
    
    def side_right(self):
        """Side tendon right (channel 6)"""
        return self.send_command("sr")
    
    def reset_position(self):
        """Reset to neutral position (includes all channels)"""
        return self.send_command("b")
    
    def open_mouth(self):
        """Open mouth"""
        return self.send_command("om")
    
    def close_mouth(self):
        """Close mouth"""
        return self.send_command("cm")
    
    def talk_animation(self):
        """Perform talking animation"""
        return self.send_command("t")
    
    def dance_animation(self):
        """Perform dance animation"""
        return self.send_command("d")
    
    def wiggle_continuous(self):
        """Perform continuous wiggle motion using side servos (channels 5 & 6)"""
        return self.send_command("w")
    
    def sadness_movement(self):
        """Perform sadness movement"""
        return self.send_command("s")
    
    def execute_movement_sequence(self, movements: list, delays: list = None):
        """Execute a sequence of movements with optional delays"""
        if delays is None:
            delays = [0.5] * len(movements)
        
        for movement, delay in zip(movements, delays):
            self.send_command(movement)
            time.sleep(delay)
    
    def is_connected(self) -> bool:
        """Check if Arduino is connected"""
        return self.connected
    
    def close(self):
        """Close serial connection"""
        if self.connected:
            self.serial_connection.close()
            print("🔌 Arduino connection closed")
    
    def test_arduino_functionality(self) -> bool:
        """Test if Arduino has the wiggle functionality"""
        if not self.connected:
            return False
            
        try:
            # Send a test command and check response
            self.serial_connection.write(b"w\n")
            time.sleep(0.2)
            
            # Read any response
            if self.serial_connection.in_waiting:
                response = self.serial_connection.readline().decode('utf-8', errors='ignore').strip()
                # If Arduino responds with wiggle motion, it has the right code
                if "wiggle" in response.lower() or "continuous" in response.lower():
                    return True
            
            # Reset to neutral after test
            self.serial_connection.write(b"b\n")
            time.sleep(0.1)
            return False
            
        except Exception as e:
            print(f"Arduino test failed: {e}")
            return False 