#!/usr/bin/env python3
"""
📝 WORM RESPONSE EDITOR
Interactive editor for managing predefined responses and testing TTS
Works independently - no AI dependencies
"""

import json
import os
import sys
import time
from typing import Dict, List, Optional
from config_manager import ConfigManager
from core.audio_controller import AudioController

class ResponseEditor:
    """Interactive editor for WORM responses with TTS testing"""
    
    def __init__(self):
        self.config = ConfigManager()
        self.audio = AudioController()
        self.running = True
        
        print("📝 WORM RESPONSE EDITOR")
        print("=" * 50)
        print("✅ Text-to-Speech ready")
        print(f"📊 Loaded {self.config.get_response_count()} existing responses")
        print()
    
    def start(self):
        """Start the interactive response editor"""
        while self.running:
            self._show_main_menu()
            choice = input("\nEnter your choice: ").strip()
            
            try:
                if choice == '1':
                    self._browse_responses()
                elif choice == '2':
                    self._add_new_response()
                elif choice == '3':
                    self._edit_response()
                elif choice == '4':
                    self._delete_response()
                elif choice == '5':
                    self._test_tts()
                elif choice == '6':
                    self._preview_response()
                elif choice == '7':
                    self._import_responses()
                elif choice == '8':
                    self._export_responses()
                elif choice == '9':
                    self._show_statistics()
                elif choice.lower() in ['q', 'quit', 'exit']:
                    self._quit()
                else:
                    print("❌ Invalid choice. Please try again.")
            except KeyboardInterrupt:
                self._quit()
            except Exception as e:
                print(f"❌ Error: {e}")
            
            input("\nPress Enter to continue...")
    
    def _show_main_menu(self):
        """Display the main menu options"""
        print("\n" + "=" * 50)
        print("📝 RESPONSE EDITOR MENU")
        print("=" * 50)
        print("1. 📖 Browse existing responses")
        print("2. ➕ Add new response")
        print("3. ✏️  Edit existing response")
        print("4. 🗑️  Delete response")
        print("5. 🎤 Test text-to-speech")
        print("6. 👀 Preview response (text + TTS)")
        print("7. 📥 Import responses from file")
        print("8. 📤 Export responses to file")
        print("9. 📊 Show statistics")
        print("Q. 🚪 Quit")
    
    def _browse_responses(self):
        """Browse all existing responses"""
        print("\n📖 BROWSING RESPONSES")
        print("-" * 30)
        
        responses = self.config.list_responses()
        
        if not responses:
            print("❌ No responses found!")
            return
        
        for category_name, category_data in responses.items():
            print(f"\n📁 {category_name.upper()}")
            
            if isinstance(category_data, dict):
                # Category has subcategories
                for subcategory_name, subcategory_responses in category_data.items():
                    print(f"  📂 {subcategory_name}")
                    if isinstance(subcategory_responses, list):
                        for i, response in enumerate(subcategory_responses):
                            text = response.get('text', 'No text')[:60]
                            movement = response.get('movement', 'none')
                            print(f"    {i+1}. {text}... (movement: {movement})")
            elif isinstance(category_data, list):
                # Category is a direct list
                for i, response in enumerate(category_data):
                    text = response.get('text', 'No text')[:60]
                    movement = response.get('movement', 'none')
                    print(f"  {i+1}. {text}... (movement: {movement})")
    
    def _add_new_response(self):
        """Add a new response to the system"""
        print("\n➕ ADD NEW RESPONSE")
        print("-" * 20)
        
        # Get category
        print("\nAvailable categories:")
        categories = list(self.config.list_responses().keys())
        for i, cat in enumerate(categories):
            print(f"  {i+1}. {cat}")
        print(f"  {len(categories)+1}. Create new category")
        
        try:
            cat_choice = int(input(f"\nSelect category (1-{len(categories)+1}): "))
            
            if cat_choice == len(categories) + 1:
                category = input("Enter new category name: ").strip()
            elif 1 <= cat_choice <= len(categories):
                category = categories[cat_choice - 1]
            else:
                print("❌ Invalid category choice")
                return
        except ValueError:
            print("❌ Invalid input")
            return
        
        # Get subcategory
        if category in self.config.responses and isinstance(self.config.responses[category], dict):
            subcategories = list(self.config.responses[category].keys())
            print(f"\nAvailable subcategories in '{category}':")
            for i, subcat in enumerate(subcategories):
                print(f"  {i+1}. {subcat}")
            print(f"  {len(subcategories)+1}. Create new subcategory")
            
            try:
                subcat_choice = int(input(f"Select subcategory (1-{len(subcategories)+1}): "))
                
                if subcat_choice == len(subcategories) + 1:
                    subcategory = input("Enter new subcategory name: ").strip()
                elif 1 <= subcat_choice <= len(subcategories):
                    subcategory = subcategories[subcat_choice - 1]
                else:
                    print("❌ Invalid subcategory choice")
                    return
            except ValueError:
                print("❌ Invalid input")
                return
        else:
            subcategory = input("Enter subcategory name: ").strip()
        
        # Get response text
        text = input("\nEnter response text: ").strip()
        if not text:
            print("❌ Response text cannot be empty")
            return
        
        # Get movement (optional)
        print("\nAvailable movements (Arduino shortcuts):")
        movements = [
            "none", "d", "t", "s", "fl", "fr", "bl", "br", "b", "om", "cm"
        ]
        movement_descriptions = [
            "none", "dance", "talk", "sadness", "forward-left", "forward-right", 
            "back-left", "back-right", "reset", "open-mouth", "close-mouth"
        ]
        
        for i, (movement, desc) in enumerate(zip(movements, movement_descriptions)):
            print(f"  {i+1}. {movement} ({desc})")
        
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
        
        # Preview before adding
        print(f"\n👀 PREVIEW:")
        print(f"Category: {category}")
        print(f"Subcategory: {subcategory}")
        print(f"Text: {text}")
        print(f"Movement: {movement or 'none'}")
        
        # Test TTS if desired
        if input("\n🎤 Test text-to-speech? (y/n): ").lower().startswith('y'):
            print("🗣️ Playing text-to-speech...")
            self.audio.speak(text, blocking=True)
        
        # Confirm addition
        if input("\n✅ Add this response? (y/n): ").lower().startswith('y'):
            success = self.config.add_response(category, subcategory, text, movement)
            if success:
                print("✅ Response added successfully!")
            else:
                print("❌ Failed to add response")
        else:
            print("❌ Response not added")
    
    def _edit_response(self):
        """Edit an existing response"""
        print("\n✏️ EDIT RESPONSE")
        print("-" * 15)
        
        # This is a simplified version - in a full implementation you'd want
        # to select specific responses to edit
        print("📝 For now, you can:")
        print("1. Delete the response you want to change")
        print("2. Add a new response with the updated text")
        print("\n💡 Future versions will support direct editing")
    
    def _delete_response(self):
        """Delete an existing response"""
        print("\n🗑️ DELETE RESPONSE")
        print("-" * 15)
        
        category = input("Enter category name: ").strip()
        subcategory = input("Enter subcategory name: ").strip()
        
        try:
            index = int(input("Enter response index (1-based): ")) - 1
            success = self.config.remove_response(category, subcategory, index)
            if success:
                print("✅ Response deleted successfully!")
            else:
                print("❌ Failed to delete response")
        except ValueError:
            print("❌ Invalid index")
    
    def _test_tts(self):
        """Test text-to-speech with custom text"""
        print("\n🎤 TEXT-TO-SPEECH TEST")
        print("-" * 25)
        
        while True:
            text = input("\nEnter text to speak (or 'back' to return): ").strip()
            
            if text.lower() in ['back', 'return', 'exit']:
                break
            
            if not text:
                print("❌ Please enter some text")
                continue
            
            print("🗣️ Playing text-to-speech...")
            
            # Test different speeds
            speed_choice = input("Choose speed (1=slow, 2=normal, 3=fast): ").strip()
            
            if speed_choice == '1':
                self.audio.speak(text, speed=80, blocking=True)
            elif speed_choice == '3':
                self.audio.speak(text, speed=200, blocking=True)
            else:
                self.audio.speak(text, speed=150, blocking=True)
            
            print("✅ Playback complete!")
    
    def _preview_response(self):
        """Preview a response with TTS"""
        print("\n👀 PREVIEW RESPONSE")
        print("-" * 20)
        
        query = input("Enter a query to find matching response: ").strip()
        
        if not query:
            print("❌ Please enter a query")
            return
        
        response = self.config.find_response(query)
        
        if not response:
            print(f"❌ No response found for '{query}'")
            return
        
        print(f"\n📖 Found response:")
        print(f"Text: {response.text}")
        print(f"Movement: {response.movement or 'none'}")
        
        if input("\n🎤 Play with text-to-speech? (y/n): ").lower().startswith('y'):
            print("🗣️ Playing response...")
            self.audio.speak(response.text, blocking=True)
            print("✅ Playback complete!")
    
    def _import_responses(self):
        """Import responses from a JSON file"""
        print("\n📥 IMPORT RESPONSES")
        print("-" * 20)
        
        filename = input("Enter filename to import from: ").strip()
        
        if not os.path.exists(filename):
            print(f"❌ File '{filename}' not found")
            return
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                imported_data = json.load(f)
            
            # Merge with existing responses
            if input(f"🔄 Merge with existing responses? (y/n): ").lower().startswith('y'):
                for category, category_data in imported_data.items():
                    if category not in self.config.responses:
                        self.config.responses[category] = {}
                    
                    if isinstance(category_data, dict):
                        for subcategory, responses in category_data.items():
                            if subcategory not in self.config.responses[category]:
                                self.config.responses[category][subcategory] = []
                            self.config.responses[category][subcategory].extend(responses)
                
                self.config.save_responses()
                print("✅ Responses imported and merged!")
            
        except Exception as e:
            print(f"❌ Import failed: {e}")
    
    def _export_responses(self):
        """Export responses to a JSON file"""
        print("\n📤 EXPORT RESPONSES")
        print("-" * 20)
        
        filename = input("Enter filename to export to (e.g., my_responses.json): ").strip()
        
        if not filename.endswith('.json'):
            filename += '.json'
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.config.responses, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Responses exported to '{filename}'!")
            
        except Exception as e:
            print(f"❌ Export failed: {e}")
    
    def _show_statistics(self):
        """Show response statistics"""
        print("\n📊 RESPONSE STATISTICS")
        print("-" * 25)
        
        stats = self.config.get_stats()
        print(f"Total responses: {stats['total_responses']}")
        print(f"Categories: {stats['categories']}")
        print(f"File: {self.config.responses_file}")
        
        # Count by category
        print(f"\nBreakdown by category:")
        for category_name, category_data in self.config.responses.items():
            count = 0
            if isinstance(category_data, dict):
                for subcategory in category_data.values():
                    if isinstance(subcategory, list):
                        count += len(subcategory)
            elif isinstance(category_data, list):
                count = len(category_data)
            
            print(f"  {category_name}: {count} responses")
    
    def _quit(self):
        """Quit the response editor"""
        print("\n👋 Closing response editor...")
        self.audio.close()
        self.running = False
        print("✅ Response editor closed!")

def main():
    """Main entry point for response editor"""
    try:
        editor = ResponseEditor()
        editor.start()
    except KeyboardInterrupt:
        print("\n\n👋 Response editor interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main() 