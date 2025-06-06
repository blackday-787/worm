#!/usr/bin/env python3
"""
WORM STARTUP SCRIPT
Simple startup - text mode default, type 'voice' to switch to voice mode
"""

import sys
from worm_system_refactored import WormSystem

def main():
    """Start WORM system"""
    print("WORM ROBOT STARTING...")
    print("=" * 40)
    
    try:
        # Initialize and start in text mode (default)
        worm = WormSystem()
        
        print("\nTEXT MODE (default)")
        print("Type 'voice' to switch to voice mode")
        print("Type 'quit' to exit")
        print("-" * 40)
        
        # Start main loop
        worm.running = True
        
        while worm.running:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'stop']:
                    break
                elif user_input.lower() == 'voice':
                    print("Switching to VOICE mode...")
                    print("Say 'worm' to get my attention")
                    print("Press Ctrl+C to return to text mode")
                    try:
                        worm.start(voice_mode=True)
                    except KeyboardInterrupt:
                        print("\nReturning to TEXT mode...")
                        continue
                elif user_input:
                    worm._process_input(user_input)
                    
            except KeyboardInterrupt:
                print("\nBack to TEXT mode")
                continue
                
        worm.stop()
        
    except Exception as e:
        print(f"Error: {e}")
        if 'worm' in locals():
            worm.stop()

if __name__ == "__main__":
    main() 