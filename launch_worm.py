#!/usr/bin/env python3
"""
🚀 FAST WORM LAUNCHER
Quick startup validation and optimized launch
"""

import sys
import os
import subprocess
import time

def main():
    """Fast launch with validation"""
    print("🐛 WORM SYSTEM FAST LAUNCHER")
    print("━" * 40)
    
    # Quick essential checks (no detailed validation)
    start_time = time.time()
    
    # Check if config file exists (critical)
    if not os.path.exists("worm_responses.json"):
        print("❌ worm_responses.json missing!")
        print("💡 Run: python3 startup_check.py for full diagnostics")
        return False
    
    # Quick package check (only critical ones)
    try:
        import pygame
        import openai
        import gtts
        print("✅ Core packages available")
    except ImportError as e:
        print(f"❌ Missing critical package: {e}")
        print("💡 Run: python3 startup_check.py for full diagnostics")
        return False
    
    elapsed = time.time() - start_time
    print(f"⚡ Startup validation: {elapsed:.2f}s")
    
    # Launch the optimized system
    print("🚀 Launching WORM system...")
    try:
        from worm_system import WormController
        controller = WormController()
        controller.run()
    except KeyboardInterrupt:
        print("\n👋 Shutdown by user")
    except Exception as e:
        print(f"❌ System error: {e}")
        print("💡 Run: python3 startup_check.py for diagnostics")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 