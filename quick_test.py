#!/usr/bin/env python3
"""
Quick diagnostic for Arduino communication and wiggle functionality
"""

from core.worm_controller import WormController
import time

def main():
    print("🔧 Quick Arduino Diagnostic")
    print("=" * 30)
    
    controller = WormController()
    
    print(f"Connected: {controller.is_connected()}")
    print(f"Simulation mode: {controller.simulation_mode}")
    
    if controller.is_connected():
        print("\n📡 Testing basic communication...")
        
        # Test basic reset
        print("1. Testing reset command 'b'...")
        result = controller.send_command("b")
        print(f"   Result: {result}")
        time.sleep(1)
        
        # Test if Arduino recognizes wiggle command
        print("2. Testing wiggle command 'w'...")
        result = controller.send_command("w")
        print(f"   Result: {result}")
        time.sleep(1)
        
        # Test individual channel commands
        print("3. Testing individual channels...")
        print("   Testing SR (channel 5)...")
        result = controller.send_command("tsr")
        print(f"   Result: {result}")
        time.sleep(2)
        
        print("   Testing SL (channel 6)...")
        result = controller.send_command("tsl")
        print(f"   Result: {result}")
        time.sleep(2)
        
        print("4. Resetting to neutral...")
        controller.send_command("b")
        
    else:
        print("❌ Arduino not connected - cannot test hardware")
    
    print("\n✅ Quick test complete!")

if __name__ == "__main__":
    main() 