#!/usr/bin/env python3
"""
🛠️ WORM RESPONSE EDITOR
Simple tool to edit worm responses without touching the main code
"""

import json
import os
from pathlib import Path

def load_responses():
    """Load current responses"""
    try:
        with open("worm_responses.json", 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ worm_responses.json not found!")
        return None

def save_responses(responses):
    """Save responses back to file"""
    with open("worm_responses.json", 'w') as f:
        json.dump(responses, f, indent=2)
    print("✅ Responses saved!")

def edit_startup_message():
    """Edit the startup message"""
    responses = load_responses()
    if not responses:
        return
    
    print("\n🎤 EDITING STARTUP MESSAGE")
    print("━" * 40)
    print("This is what the worm SAYS when it first starts up.")
    print("It's spoken automatically - no trigger needed.")
    
    current = responses["startup_message"]
    word_count = len(current.split())
    movement_info = "1 mouth movement" if word_count <= 5 else "2 mouth movements"
    
    print(f"\nCurrent startup message ({word_count} words, {movement_info}):")
    print(f"'{current}'")
    
    new_message = input("\nEnter new startup message (or press Enter to keep current): ").strip()
    
    if new_message:
        new_word_count = len(new_message.split())
        new_movement_info = "1 mouth movement" if new_word_count <= 5 else "2 mouth movements"
        
        print(f"\n🎯 Your new message: '{new_message}'")
        print(f"📊 {new_word_count} words = {new_movement_info}")
        
        confirm = input("Save this message? (y/n): ").strip().lower()
        if confirm == 'y':
            responses["startup_message"] = new_message
            save_responses(responses)
            print(f"🎉 Startup message changed!")
        else:
            print("No changes made.")
    else:
        print("No changes made.")

def edit_existing_response():
    """Edit an existing response"""
    responses = load_responses()
    if not responses:
        return
    
    print("\n📝 EDIT EXISTING RESPONSE")
    print("━" * 40)
    
    if not responses.get("responses"):
        print("❌ No responses found!")
        return
    
    # Show all responses
    response_list = list(responses["responses"].items())
    
    print(f"📋 Available responses ({len(response_list)} total):")
    for i, (key, data) in enumerate(response_list, 1):
        speech = data["speech"]
        movement = data["movement"]
        mouth_movements = data.get("mouth_movements", 1)  # Default to 1 if not set
        word_count = len(speech.split())
        
        # Make key readable
        readable_key = key.replace("_", " ")
        
        print(f"  {i}. '{readable_key}' → '{speech}' [{movement}] ({mouth_movements}t) ({word_count} words)")
    
    try:
        choice = input(f"\nSelect response to edit (1-{len(response_list)}): ").strip()
        index = int(choice) - 1
        
        if 0 <= index < len(response_list):
            key, data = response_list[index]
            edit_single_response(responses, key, data)
        else:
            print("❌ Invalid response number!")
    except ValueError:
        print("❌ Please enter a valid number!")

def edit_single_response(responses, key, data):
    """Edit a single response"""
    current_speech = data["speech"]
    current_movement = data["movement"]
    current_mouth_movements = data.get("mouth_movements", 1)  # Default to 1 if not set
    word_count = len(current_speech.split())
    
    readable_key = key.replace("_", " ")
    
    print(f"\n🎯 EDITING: {readable_key}")
    print(f"Current input trigger: '{readable_key}'")
    print(f"Current speech output: '{current_speech}' ({word_count} words)")
    print(f"Current movement: {current_movement}")
    print(f"Current mouth movements: {current_mouth_movements}t")
    
    print("\n1. Edit input trigger only")
    print("2. Edit speech output only")
    print("3. Edit movement only") 
    print("4. Edit mouth movements only")
    print("5. Edit input trigger + speech output")
    print("6. Edit speech output + movement")
    print("7. Edit speech output + mouth movements")
    print("8. Edit movement + mouth movements")
    print("9. Edit all (trigger + speech + movement + mouth movements)")
    print("10. Cancel")
    
    choice = input("Choose option (1-10): ").strip()
    
    if choice == "1":
        new_trigger = input(f"\nEnter new input trigger (currently '{readable_key}'): ").strip()
        if new_trigger:
            new_key = new_trigger.replace(" ", "_").lower()
            if new_key != key and new_key in responses["responses"]:
                print(f"❌ Trigger '{new_trigger}' already exists!")
                return
            
            if input(f"Change trigger from '{readable_key}' to '{new_trigger}'? (y/n): ").lower() == 'y':
                # Remove old key and add new one
                responses["responses"][new_key] = responses["responses"].pop(key)
                save_responses(responses)
                print("🎉 Input trigger updated!")
    
    elif choice == "2":
        new_speech = input(f"\nEnter new speech output: ").strip()
        if new_speech:
            new_word_count = len(new_speech.split())
            print(f"Preview: '{new_speech}' ({new_word_count} words)")
            
            if input("Save? (y/n): ").lower() == 'y':
                responses["responses"][key]["speech"] = new_speech
                save_responses(responses)
                print("🎉 Speech output updated!")
    
    elif choice == "3":
        print("\nAvailable movements: fl, fr, bl, br, b, om, cm, t, d, choreographedTalk, sadness")
        new_movement = input("Enter new movement: ").strip()
        if new_movement:
            if input(f"Set movement to '{new_movement}'? (y/n): ").lower() == 'y':
                responses["responses"][key]["movement"] = new_movement
                save_responses(responses)
                print("🎉 Movement updated!")
    
    elif choice == "4":
        print("\nMouth movements control how many 't' commands are sent during speech")
        print("1t = single mouth movement, 2t = double mouth movement, etc.")
        new_mouth = input(f"Enter mouth movements (currently {current_mouth_movements}t): ").strip()
        if new_mouth:
            try:
                mouth_count = int(new_mouth.replace('t', ''))
                if mouth_count >= 0:
                    if input(f"Set mouth movements to {mouth_count}t? (y/n): ").lower() == 'y':
                        responses["responses"][key]["mouth_movements"] = mouth_count
                        save_responses(responses)
                        print("🎉 Mouth movements updated!")
                else:
                    print("❌ Mouth movements must be 0 or greater!")
            except ValueError:
                print("❌ Please enter a valid number!")
    
    elif choice == "5":
        new_trigger = input(f"\nEnter new input trigger (currently '{readable_key}'): ").strip()
        if new_trigger:
            new_speech = input("Enter new speech output: ").strip()
            if new_speech:
                new_key = new_trigger.replace(" ", "_").lower()
                if new_key != key and new_key in responses["responses"]:
                    print(f"❌ Trigger '{new_trigger}' already exists!")
                    return
                
                new_word_count = len(new_speech.split())
                
                print(f"\nPreview:")
                print(f"Input trigger: '{new_trigger}'")
                print(f"Speech output: '{new_speech}' ({new_word_count} words)")
                
                if input("Save both? (y/n): ").lower() == 'y':
                    # Remove old key and add new one with new speech
                    old_data = responses["responses"].pop(key)
                    responses["responses"][new_key] = {
                        "speech": new_speech,
                        "movement": old_data["movement"],
                        "mouth_movements": old_data.get("mouth_movements", 1)
                    }
                    save_responses(responses)
                    print("🎉 Input trigger and speech updated!")
    
    elif choice == "6":
        new_speech = input(f"\nEnter new speech output: ").strip()
        if new_speech:
            print("\nAvailable movements: fl, fr, bl, br, b, om, cm, t, d, choreographedTalk, sadness")
            new_movement = input("Enter new movement: ").strip()
            if new_movement:
                new_word_count = len(new_speech.split())
                
                print(f"\nPreview:")
                print(f"Speech output: '{new_speech}' ({new_word_count} words)")
                print(f"Movement: {new_movement}")
                
                if input("Save both? (y/n): ").lower() == 'y':
                    responses["responses"][key]["speech"] = new_speech
                    responses["responses"][key]["movement"] = new_movement
                    save_responses(responses)
                    print("🎉 Speech and movement updated!")
    
    elif choice == "7":
        new_speech = input(f"\nEnter new speech output: ").strip()
        if new_speech:
            print("\nMouth movements control how many 't' commands are sent during speech")
            new_mouth = input(f"Enter mouth movements (currently {current_mouth_movements}t): ").strip()
            if new_mouth:
                try:
                    mouth_count = int(new_mouth.replace('t', ''))
                    if mouth_count >= 0:
                        new_word_count = len(new_speech.split())
                        
                        print(f"\nPreview:")
                        print(f"Speech output: '{new_speech}' ({new_word_count} words)")
                        print(f"Mouth movements: {mouth_count}t")
                        
                        if input("Save both? (y/n): ").lower() == 'y':
                            responses["responses"][key]["speech"] = new_speech
                            responses["responses"][key]["mouth_movements"] = mouth_count
                            save_responses(responses)
                            print("🎉 Speech and mouth movements updated!")
                    else:
                        print("❌ Mouth movements must be 0 or greater!")
                except ValueError:
                    print("❌ Please enter a valid number!")
    
    elif choice == "8":
        print("\nAvailable movements: fl, fr, bl, br, b, om, cm, t, d, choreographedTalk, sadness")
        new_movement = input("Enter new movement: ").strip()
        if new_movement:
            print("\nMouth movements control how many 't' commands are sent during speech")
            new_mouth = input(f"Enter mouth movements (currently {current_mouth_movements}t): ").strip()
            if new_mouth:
                try:
                    mouth_count = int(new_mouth.replace('t', ''))
                    if mouth_count >= 0:
                        print(f"\nPreview:")
                        print(f"Movement: {new_movement}")
                        print(f"Mouth movements: {mouth_count}t")
                        
                        if input("Save both? (y/n): ").lower() == 'y':
                            responses["responses"][key]["movement"] = new_movement
                            responses["responses"][key]["mouth_movements"] = mouth_count
                            save_responses(responses)
                            print("🎉 Movement and mouth movements updated!")
                    else:
                        print("❌ Mouth movements must be 0 or greater!")
                except ValueError:
                    print("❌ Please enter a valid number!")
    
    elif choice == "9":
        new_trigger = input(f"\nEnter new input trigger (currently '{readable_key}'): ").strip()
        if new_trigger:
            new_speech = input("Enter new speech output: ").strip()
            if new_speech:
                print("\nAvailable movements: fl, fr, bl, br, b, om, cm, t, d, choreographedTalk, sadness")
                new_movement = input("Enter new movement: ").strip()
                if new_movement:
                    print("\nMouth movements control how many 't' commands are sent during speech")
                    new_mouth = input(f"Enter mouth movements (currently {current_mouth_movements}t): ").strip()
                    if new_mouth:
                        try:
                            mouth_count = int(new_mouth.replace('t', ''))
                            if mouth_count >= 0:
                                new_key = new_trigger.replace(" ", "_").lower()
                                if new_key != key and new_key in responses["responses"]:
                                    print(f"❌ Trigger '{new_trigger}' already exists!")
                                    return
                                
                                new_word_count = len(new_speech.split())
                                
                                print(f"\nPreview:")
                                print(f"Input trigger: '{new_trigger}'")
                                print(f"Speech output: '{new_speech}' ({new_word_count} words)")
                                print(f"Movement: {new_movement}")
                                print(f"Mouth movements: {mouth_count}t")
                                
                                if input("Save all? (y/n): ").lower() == 'y':
                                    # Remove old key and add completely new one
                                    responses["responses"].pop(key)
                                    responses["responses"][new_key] = {
                                        "speech": new_speech,
                                        "movement": new_movement,
                                        "mouth_movements": mouth_count
                                    }
                                    save_responses(responses)
                                    print("🎉 All fields updated!")
                            else:
                                print("❌ Mouth movements must be 0 or greater!")
                        except ValueError:
                            print("❌ Please enter a valid number!")
    
    elif choice == "10":
        print("❌ No changes made.")
    else:
        print("❌ Invalid choice!")

def add_new_response():
    """Add a new response"""
    responses = load_responses()
    if not responses:
        return
    
    print("\n✨ ADD NEW RESPONSE")
    print("━" * 40)
    
    # Get key
    key = input("Enter response key (use_underscores_for_spaces): ").strip()
    if not key:
        print("❌ Key cannot be empty!")
        return
    
    if key in responses["responses"]:
        print(f"❌ Key '{key}' already exists!")
        return
    
    # Get speech
    speech = input("Enter speech output: ").strip()
    if not speech:
        print("❌ Speech cannot be empty!")
        return
    
    # Get movement
    print("\nAvailable movements: fl, fr, bl, br, b, om, cm, t, d, choreographedTalk, sadness")
    movement = input("Enter movement (default 't'): ").strip()
    if not movement:
        movement = "t"
    
    # Get mouth movements
    print("\nMouth movements control how many 't' commands are sent during speech")
    print("1t = single mouth movement, 2t = double mouth movement, etc.")
    mouth_input = input("Enter mouth movements (default '1t'): ").strip()
    if not mouth_input:
        mouth_movements = 1
    else:
        try:
            mouth_movements = int(mouth_input.replace('t', ''))
            if mouth_movements < 0:
                print("❌ Mouth movements must be 0 or greater! Using default 1t.")
                mouth_movements = 1
        except ValueError:
            print("❌ Invalid mouth movements! Using default 1t.")
            mouth_movements = 1
    
    # Preview
    word_count = len(speech.split())
    readable_key = key.replace("_", " ")
    
    print(f"\n🎯 PREVIEW:")
    print(f"Key: '{readable_key}'")
    print(f"Speech: '{speech}' ({word_count} words)")
    print(f"Movement: {movement}")
    print(f"Mouth movements: {mouth_movements}t")
    
    if input("\nSave this response? (y/n): ").lower() == 'y':
        responses["responses"][key] = {
            "speech": speech,
            "movement": movement,
            "mouth_movements": mouth_movements
        }
        save_responses(responses)
        print(f"🎉 Added new response!")

def main():
    """Main menu"""
    while True:
        print("\n🐛 WORM RESPONSE EDITOR")
        print("1. Edit existing response")
        print("2. Add new response") 
        print("3. Edit startup message")
        print("4. Quit")
        
        choice = input("\nChoose option (1-4): ").strip()
        
        if choice == "1":
            edit_existing_response()
        elif choice == "2":
            add_new_response()
        elif choice == "3":
            edit_startup_message()
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main() 