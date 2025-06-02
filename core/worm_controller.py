"""
🤖 WORM HARDWARE CONTROLLER
Pure hardware control - no AI dependencies
Handles Arduino communication and servo movements
"""

import serial
import time
import os
from typing import Optional, Dict, Any

class WormController:
    """Pure hardware controller for the worm robot"""
    
    def __init__(self):
        self.arduino = None
        self.setup_serial()
        
    def setup_serial(self):
        """Initialize Arduino serial connection with auto-detection"""
        # Try environment variable first
        port = os.getenv("WORM_SERIAL_PORT")
        baud = int(os.getenv("WORM_BAUD_RATE", "115200"))
        
        # Common Arduino ports for macOS/Linux
        common_ports = [
            "/dev/cu.usbmodem1401",
            "/dev/cu.usbmodem1301", 
            "/dev/cu.usbmodem101",
            "/dev/cu.usbmodem14101",
            "/dev/ttyUSB0",
            "/dev/ttyACM0"
        ]
        
        # If no specific port set, try to find one
        if not port:
            for test_port in common_ports:
                if os.path.exists(test_port):
                    port = test_port
                    break
        
        if not port:
            print("⚠️  No Arduino port found - running in simulation mode")
            self.arduino = None
            return
        
        try:
            self.arduino = serial.Serial(port, baud, timeout=1)
            time.sleep(2)  # Wait for Arduino to initialize
            print(f"✅ Arduino connected on {port}")
        except Exception as e:
            print(f"⚠️  Arduino connection failed on {port}: {e}")
            print("🤖 Running in simulation mode")
            self.arduino = None
    
    def send_command(self, command: str) -> bool:
        """Send command to Arduino and return success status"""
        if not self.arduino:
            print(f"🤖 [SIMULATION] Arduino command: {command}")
            return True
            
        try:
            self.arduino.write(f"{command}\n".encode())
            print(f"🤖 Sent to Arduino: {command}")
            
            # Read Arduino response if available
            time.sleep(0.1)
            if self.arduino.in_waiting:
                response = self.arduino.readline().decode().strip()
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
    
    def reset_position(self):
        """Reset to neutral position"""
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
    
    def choreographed_talk(self):
        """Perform choreographed talking animation"""
        return self.send_command("choreographedTalk")
    
    def sadness_movement(self):
        """Perform sadness movement"""
        return self.send_command("sadness")
    
    def execute_movement_sequence(self, movements: list, delays: list = None):
        """Execute a sequence of movements with optional delays"""
        if delays is None:
            delays = [0.5] * len(movements)
        
        for movement, delay in zip(movements, delays):
            self.send_command(movement)
            time.sleep(delay)
    
    def is_connected(self) -> bool:
        """Check if Arduino is connected"""
        return self.arduino is not None
    
    def close(self):
        """Close serial connection"""
        if self.arduino:
            self.arduino.close()
            print("🔌 Arduino connection closed") 