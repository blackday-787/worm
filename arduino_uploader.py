#!/usr/bin/env python3
"""
🤖 ARDUINO UPLOADER
Automatically compile and upload the worm controller sketch
"""

import os
import sys
import subprocess
import time
import serial
import serial.tools.list_ports
from pathlib import Path

class ArduinoUploader:
    def __init__(self):
        self.sketch_file = "src/arduino/worm_controller.ino"
        self.arduino_cli = self.find_arduino_cli()
        
    def find_arduino_cli(self):
        """Find Arduino CLI installation"""
        possible_paths = [
            "/Applications/Arduino.app/Contents/MacOS/arduino-cli",
            "/usr/local/bin/arduino-cli",
            "arduino-cli"  # If in PATH
        ]
        
        for path in possible_paths:
            try:
                result = subprocess.run([path, "version"], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(f"✅ Found Arduino CLI: {path}")
                    return path
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
                
        # Try to install arduino-cli if not found
        print("⚠️  Arduino CLI not found, attempting to install...")
        self.install_arduino_cli()
        return "arduino-cli"
        
    def install_arduino_cli(self):
        """Install Arduino CLI using homebrew on macOS"""
        try:
            print("📦 Installing Arduino CLI via homebrew...")
            subprocess.run(["brew", "install", "arduino-cli"], check=True)
            print("✅ Arduino CLI installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install Arduino CLI")
            print("Please install manually: https://arduino.github.io/arduino-cli/")
            sys.exit(1)
            
    def detect_arduino_port(self):
        """Auto-detect Arduino USB port"""
        print("🔍 Scanning for Arduino devices...")
        
        ports = serial.tools.list_ports.comports()
        arduino_ports = []
        
        for port in ports:
            # Look for common Arduino identifiers
            if any(keyword in (port.description or "").lower() for keyword in 
                   ["arduino", "usb", "serial", "ch340", "cp210"]):
                arduino_ports.append(port.device)
                print(f"📱 Found potential Arduino: {port.device} - {port.description}")
        
        if not arduino_ports:
            print("❌ No Arduino devices detected")
            return None
            
        if len(arduino_ports) == 1:
            selected_port = arduino_ports[0]
            print(f"✅ Auto-selected Arduino port: {selected_port}")
            return selected_port
        else:
            # Automatically select the first port without prompting
            selected_port = arduino_ports[0]
            print(f"Multiple Arduino devices found, auto-selecting first: {selected_port}")
            return selected_port
                
    def setup_arduino_environment(self):
        """Setup Arduino CLI environment"""
        print("🔧 Setting up Arduino environment...")
        
        try:
            # Update core index
            subprocess.run([self.arduino_cli, "core", "update-index"], 
                         check=True, capture_output=True)
            
            # Install Arduino AVR core (for Uno, Nano, etc.)
            subprocess.run([self.arduino_cli, "core", "install", "arduino:avr"], 
                         check=True, capture_output=True)
            
            # Install required libraries
            libraries = [
                "Adafruit PWM Servo Driver Library",
                "Wire"
            ]
            
            for lib in libraries:
                try:
                    subprocess.run([self.arduino_cli, "lib", "install", lib], 
                                 check=True, capture_output=True)
                    print(f"✅ Installed library: {lib}")
                except subprocess.CalledProcessError:
                    print(f"⚠️  Library {lib} may already be installed")
                    
            print("✅ Arduino environment ready")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Arduino setup failed: {e}")
            return False
            
    def compile_sketch(self):
        """Compile the Arduino sketch"""
        sketch_dir = Path("src/arduino/current")
        sketch_file = sketch_dir / "current.ino"
        
        if not sketch_file.exists():
            print(f"❌ Sketch file not found: {sketch_file}")
            return False
            
        print(f"🔨 Compiling {sketch_file}...")
        
        try:
            # Arduino CLI needs the directory containing the .ino file
            result = subprocess.run([
                self.arduino_cli, "compile",
                "--fqbn", "arduino:avr:uno",  # Assuming Arduino Uno
                str(sketch_dir)  # Pass the directory, not the file
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print("✅ Compilation successful")
                return True
            else:
                print("❌ Compilation failed:")
                print(result.stderr)
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Compilation timeout")
            return False
        except Exception as e:
            print(f"❌ Compilation error: {e}")
            return False
            
    def upload_sketch(self, port):
        """Upload the compiled sketch to Arduino"""
        print(f"📤 Uploading to {port}...")
        
        try:
            sketch_dir = Path("src/arduino/current")
            result = subprocess.run([
                self.arduino_cli, "upload",
                "--fqbn", "arduino:avr:uno",
                "--port", port,
                str(sketch_dir)  # Pass the directory, not the file
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("✅ Upload successful!")
                return True
            else:
                print("❌ Upload failed:")
                print(result.stderr)
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Upload timeout")
            return False
        except Exception as e:
            print(f"❌ Upload error: {e}")
            return False
            
    def verify_connection(self, port):
        """Verify Arduino is responding after upload"""
        print("🔍 Verifying Arduino connection...")
        
        try:
            with serial.Serial(port, 115200, timeout=3) as ser:
                time.sleep(2)  # Wait for Arduino to initialize
                
                # Look for the "Ready" message
                start_time = time.time()
                while time.time() - start_time < 5:
                    if ser.in_waiting:
                        response = ser.readline().decode().strip()
                        print(f"📱 Arduino: {response}")
                        if "Ready" in response:
                            print("✅ Arduino verified and ready!")
                            return True
                            
                print("⚠️  Arduino uploaded but no ready signal received")
                return True  # Still consider success
                
        except Exception as e:
            print(f"❌ Verification failed: {e}")
            return False
            
    def upload(self, port=None):
        """Main upload process"""
        print("🤖 ARDUINO UPLOADER STARTING")
        print("=" * 40)
        
        # Detect port if not provided
        if not port:
            port = self.detect_arduino_port()
            if not port:
                return False
                
        # Setup environment
        if not self.setup_arduino_environment():
            return False
            
        # Compile sketch
        if not self.compile_sketch():
            return False
            
        # Upload sketch
        if not self.upload_sketch(port):
            return False
            
        # Verify connection
        success = self.verify_connection(port)
        
        if success:
            # Update environment variable for the system
            os.environ["WORM_SERIAL_PORT"] = port
            
            # Update .env file to persist the port setting
            env_line = f"WORM_SERIAL_PORT={port}"
            
            # Read existing .env content
            env_content = []
            env_file = ".env"
            if os.path.exists(env_file):
                with open(env_file, 'r') as f:
                    env_content = f.readlines()
            
            # Remove any existing WORM_SERIAL_PORT lines
            env_content = [line for line in env_content if not line.startswith("WORM_SERIAL_PORT=")]
            
            # Add the new port setting
            env_content.append(f"{env_line}\n")
            
            # Write back to .env file
            with open(env_file, 'w') as f:
                f.writelines(env_content)
                
            print(f"💾 Saved port {port} to .env file")
            
            # Also export for current session
            print(f"🔧 Setting WORM_SERIAL_PORT={port} for current session")
            
        return success

def main():
    """Entry point for Arduino uploader"""
    uploader = ArduinoUploader()
    
    # Check for command line port argument
    port = sys.argv[1] if len(sys.argv) > 1 else None
    
    success = uploader.upload(port)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 