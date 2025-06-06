#!/usr/bin/env python3
"""
RESPONSE EDITOR
Create and edit WORM responses with input/output and movement commands
"""

import json
import os
from typing import Dict, List, Optional
from config_manager import ConfigManager
from core.audio_controller import AudioController

class SimpleResponseEditor:
    """Simple response editor for creating and editing responses"""
    
    def __init__(self):
        self.config = ConfigManager()
        self.audio = AudioController()
        
    def start(self):
        """Start the response editor"""
        print("WORM RESPONSE EDITOR")
        print("=" * 30)
        
        while True:
            print("\n1. Create new response")
            print("2. Edit existing response")
            print("3. List all responses")
            print("4. Quit")
            
            choice = input("\nChoice (1-4): ").strip()
            
            if choice == '1':
                self.create_response()
            elif choice == '2':
                self.edit_response()
            elif choice == '3':
                self.list_responses()
            elif choice == '4':
                break
            else:
                print("Invalid choice")
                
        self.audio.close()
        print("Response editor closed")
    
    def create_response(self):
        """Create a new response"""
        print("\nCREATE NEW RESPONSE")
        print("-" * 20)
        
        # Get input text (what user says)
        input_text = input("Input text (what user says): ").strip()
        if not input_text:
            print("Input cannot be empty")
            return
            
        # Get output text (what WORM says)
        output_text = input("Output text (what WORM says): ").strip()
        if not output_text:
            print("Output cannot be empty")
            return
            
        # Get movement command
        print("\nMovement commands:")
        movements = ["none", "d", "s", "fl", "fr", "bl", "br", "sl", "sr", "b", "om", "cm"]
        for i, movement in enumerate(movements):
            print(f"  {i+1}. {movement}")
            
        try:
            move_choice = int(input(f"Select movement (1-{len(movements)}): "))
            if 1 <= move_choice <= len(movements):
                movement = movements[move_choice - 1]
                if movement == "none":
                    movement = None
            else:
                movement = None
        except ValueError:
            movement = None
            
        # Preview
        print(f"\nPREVIEW:")
        print(f"Input: {input_text}")
        print(f"Output: {output_text}")
        print(f"Movement: {movement or 'none'}")
        
        # Save
        if input("Save this response? (y/n): ").lower().startswith('y'):
            self.save_simple_response(input_text, output_text, movement)
            print("Response saved!")
        else:
            print("Response not saved")
    
    def edit_response(self):
        """Edit an existing response"""
        print("\nEDIT EXISTING RESPONSE")
        print("-" * 22)
        
        # Show all responses with numbers
        responses = self.get_all_responses()
        
        if not responses:
            print("No responses found")
            return
            
        print("Select response to edit:")
        for i, (trigger, output_text, movement) in enumerate(responses):
            print(f"{i+1}. Input: {trigger[:30]}... -> Output: {output_text[:30]}...")
            
        try:
            choice = int(input(f"Response number (1-{len(responses)}): ")) - 1
            if 0 <= choice < len(responses):
                old_trigger, old_output, old_movement = responses[choice]
                print(f"\nEditing response:")
                print(f"Input: {old_trigger}")
                print(f"Output: {old_output}")
                print(f"Movement: {old_movement}")
                
                # Go through creation flow with current values as defaults
                self.edit_response_flow(old_trigger, old_output, old_movement)
            else:
                print("Invalid selection")
        except ValueError:
            print("Invalid input")
    
    def edit_response_flow(self, old_trigger, old_output, old_movement):
        """Edit flow for existing response"""
        print(f"\nInput text [{old_trigger}]: ", end="")
        new_input = input().strip()
        if not new_input:
            new_input = old_trigger
            
        print(f"Output text [{old_output}]: ", end="")
        new_output = input().strip()
        if not new_output:
            new_output = old_output
                
        # Movement selection
        print("\nMovement commands:")
        movements = ["none", "d", "s", "fl", "fr", "bl", "br", "sl", "sr", "b", "om", "cm"]
        for i, movement in enumerate(movements):
            print(f"  {i+1}. {movement}")
            
        # Try to detect current movement from old_movement
        current_movement = old_movement if old_movement in movements else None
        current_idx = movements.index(current_movement) + 1 if current_movement else 1
        
        try:
            move_choice = int(input(f"Select movement [{current_idx}]: ") or current_idx)
            if 1 <= move_choice <= len(movements):
                movement = movements[move_choice - 1]
                if movement == "none":
                    movement = None
            else:
                movement = None
        except ValueError:
            movement = None
            
        print(f"\nPREVIEW:")
        print(f"Input: {new_input}")
        print(f"Output: {new_output}")
        print(f"Movement: {movement or 'none'}")
        
        # Save changes
        if input("Save changes? (y/n): ").lower().startswith('y'):
            # Remove old response and add new one
            self.remove_old_response(old_trigger)
            self.save_simple_response(new_input, new_output, movement)
            print("Response updated!")
    
    def get_all_responses(self):
        """Get all responses as a flat list with triggers"""
        responses = []
        data = self.config.list_responses()
        
        for category, category_data in data.items():
            if isinstance(category_data, dict):
                for subcategory, response_list in category_data.items():
                    if isinstance(response_list, list):
                        for response in response_list:
                            trigger = response.get('trigger', f"{category}/{subcategory}")
                            responses.append((
                                trigger,
                                response.get('text', ''),
                                response.get('movement', '')
                            ))
            elif isinstance(category_data, list):
                for response in category_data:
                    trigger = response.get('trigger', category)
                    responses.append((
                        trigger,
                        response.get('text', ''),
                        response.get('movement', '')
                    ))
        return responses
    
    def list_responses(self):
        """List all responses with input triggers"""
        responses = self.get_all_responses()
        print(f"\nALL RESPONSES ({len(responses)} total):")
        print("-" * 40)
        
        for i, (trigger, output_text, movement) in enumerate(responses):
            print(f"{i+1}. Input: {trigger}")
            print(f"   Output: {output_text[:60]}...")
            print(f"   Movement: {movement}")
            print()
    
    def save_simple_response(self, input_text, output_text, movement):
        """Save a simple response"""
        # Add to a simple "custom" category with input text as trigger
        if "custom" not in self.config.responses:
            self.config.responses["custom"] = {"user_created": []}
        
        if "user_created" not in self.config.responses["custom"]:
            self.config.responses["custom"]["user_created"] = []
            
        new_response = {
            "text": output_text,
            "movement": movement,
            "trigger": input_text.lower()
        }
        
        self.config.responses["custom"]["user_created"].append(new_response)
        self.config.save_responses()
        print(f"Added response to custom/user_created")
    
    def remove_old_response(self, trigger):
        """Remove old response by trigger"""
        if 'custom' in self.config.responses:
            for subcategory, response_list in self.config.responses['custom'].items():
                if isinstance(response_list, list):
                    for i, response in enumerate(response_list):
                        if response.get('trigger') == trigger:
                            response_list.pop(i)
                            self.config.save_responses()
                            return

def main():
    """Main entry point"""
    try:
        editor = SimpleResponseEditor()
        editor.start()
    except KeyboardInterrupt:
        print("\nResponse editor interrupted")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 