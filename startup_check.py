#!/usr/bin/env python3
"""
🚀 WORM STARTUP VALIDATOR
Quick dependency and configuration check before launching
"""

import sys
import os
import subprocess
from pathlib import Path

def check_venv():
    """Check if we're in a virtual environment"""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment detected")
        return True
    else:
        print("⚠️  Not in virtual environment - continuing anyway")
        return True  # Don't block, just warn

def check_python_packages():
    """Check required Python packages"""
    required_packages = [
        'pygame',
        'openai', 
        'gtts',
        'vosk',
        'sounddevice',
        'serial'  # pyserial
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing.append(package)
            print(f"❌ {package} - MISSING")
    
    if missing:
        print(f"\n💡 To install missing packages:")
        print(f"pip install {' '.join(missing)}")
        return False
    return True

def check_openai_key():
    """Check OpenAI API key availability"""
    key_file = Path("openai_key.txt")
    if key_file.exists():
        try:
            with open(key_file, 'r') as f:
                key = f.read().strip()
                if key and len(key) > 20:  # Basic validation
                    print("✅ OpenAI key file found")
                    return True
                else:
                    print("❌ OpenAI key file empty or invalid")
        except Exception as e:
            print(f"❌ OpenAI key file error: {e}")
    
    # Check environment variable
    env_key = os.environ.get("OPENAI_API_KEY")
    if env_key and len(env_key) > 20:
        print("✅ OpenAI key in environment")
        return True
    
    print("⚠️  No OpenAI key found - AI features will be disabled")
    return True  # Don't block startup

def check_arduino_ports():
    """Check for Arduino ports"""
    common_ports = [
        "/dev/cu.usbmodem1401",
        "/dev/cu.usbmodem1301", 
        "/dev/cu.usbmodem101",
        "/dev/ttyUSB0",
        "/dev/ttyACM0"
    ]
    
    found_ports = []
    for port in common_ports:
        if os.path.exists(port):
            found_ports.append(port)
    
    if found_ports:
        print(f"✅ Arduino ports found: {found_ports}")
        return True
    else:
        print("⚠️  No Arduino ports detected - will run in simulation mode")
        return True  # Don't block startup

def check_vosk_model():
    """Check Vosk model availability"""
    if os.path.exists("model"):
        print("✅ Vosk model found")
        return True
    else:
        print("⚠️  Vosk model missing - voice input will be disabled")
        print("💡 To download: wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip")
        return True  # Don't block startup

def check_config_files():
    """Check configuration files"""
    if os.path.exists("worm_responses.json"):
        print("✅ Response configuration found")
        return True
    else:
        print("❌ worm_responses.json missing!")
        return False

def main():
    """Run all startup checks"""
    print("🐛 WORM SYSTEM STARTUP CHECK")
    print("=" * 40)
    
    checks = [
        ("Virtual Environment", check_venv),
        ("Python Packages", check_python_packages),
        ("OpenAI API Key", check_openai_key),
        ("Arduino Ports", check_arduino_ports),
        ("Vosk Model", check_vosk_model),
        ("Config Files", check_config_files)
    ]
    
    all_critical_passed = True
    
    for name, check_func in checks:
        print(f"\n🔍 {name}:")
        try:
            result = check_func()
            if not result and name in ["Python Packages", "Config Files"]:
                all_critical_passed = False
        except Exception as e:
            print(f"❌ {name} check failed: {e}")
            if name in ["Python Packages", "Config Files"]:
                all_critical_passed = False
    
    print("\n" + "=" * 40)
    if all_critical_passed:
        print("🎉 STARTUP CHECK PASSED - Ready to launch!")
        return True
    else:
        print("❌ CRITICAL ISSUES FOUND - Fix before launching")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 