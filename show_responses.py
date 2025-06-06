#!/usr/bin/env python3
"""
📋 SHOW WORM RESPONSES
Quick reference for all current responses
"""

import json

def show_responses():
    """Display all current responses"""
    try:
        with open("worm_responses.json", 'r') as f:
            responses = json.load(f)
    except FileNotFoundError:
        print("❌ worm_responses.json not found!")
        return

    print("🐛 WORM RESPONSES REFERENCE")
    print("=" * 50)
    
    # Startup message
    startup = responses.get("startup_message", "Not set")
    word_count = len(startup.split())
    movement_info = "1 movement" if word_count <= 5 else "2 movements"
    print(f"\n🎤 STARTUP MESSAGE ({word_count} words, {movement_info}):")
    print(f"'{startup}'")
    
    # All responses
    if responses.get("responses"):
        print(f"\n📝 ALL RESPONSES ({len(responses['responses'])} total):")
        print("-" * 50)
        
        for i, (key, data) in enumerate(responses["responses"].items(), 1):
            speech = data["speech"]
            movement = data["movement"]
            mouth_movements = data.get("mouth_movements", 1)  # Default to 1 if not set
            word_count = len(speech.split())
            
            # Make key readable
            readable_key = key.replace("_", " ")
            
            print(f"{i:2d}. '{readable_key}'")
            print(f"    Speech: '{speech}' ({word_count} words)")
            print(f"    Movement: {movement}")
            print(f"    Mouth movements: {mouth_movements}t")
            print()
    else:
        print("\n❌ No responses found!")

if __name__ == "__main__":
    show_responses() 