"""
WORM CONFIGURATION MANAGER
Handles response JSON, settings, and configuration
No AI or hardware dependencies
"""

import json
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import random

@dataclass
class PredefinedResponse:
    """Structure for predefined responses"""
    text: str
    movement: Optional[str] = None
    priority: int = 1
    triggers: List[str] = None
    emotion: Optional[str] = None

class ConfigManager:
    """Manages configuration and predefined responses"""
    
    def __init__(self, responses_file: str = "worm_responses.json"):
        self.responses_file = responses_file
        self.responses = {}
        self.settings = {}
        self.load_responses()
        self.load_settings()
    
    def load_responses(self) -> bool:
        """Load predefined responses from JSON file"""
        try:
            if not os.path.exists(self.responses_file):
                print(f"Responses file {self.responses_file} not found")
                self.responses = self._create_default_responses()
                self.save_responses()
                return True
            
            with open(self.responses_file, 'r', encoding='utf-8') as f:
                self.responses = json.load(f)
            
            print(f"Loaded {len(self.responses)} response categories")
            return True
            
        except Exception as e:
            print(f"Error loading responses: {e}")
            self.responses = self._create_default_responses()
            return False
    
    def save_responses(self) -> bool:
        """Save responses to JSON file"""
        try:
            with open(self.responses_file, 'w', encoding='utf-8') as f:
                json.dump(self.responses, f, indent=2, ensure_ascii=False)
            print(f"Responses saved to {self.responses_file}")
            return True
        except Exception as e:
            print(f"Error saving responses: {e}")
            return False
    
    def _create_default_responses(self) -> Dict:
        """Create default response structure"""
        return {
            "fallbacks": [
                {"text": "I'm not sure how to respond to that, but I'm always learning!", "movement": None}
            ]
        }
    
    def find_response(self, query: str, category: str = None) -> Optional[PredefinedResponse]:
        """Find a matching predefined response"""
        query_lower = query.lower().strip()
        
        # For custom responses, try to find exact trigger matches
        if 'custom' in self.responses:
            for subcategory, response_list in self.responses['custom'].items():
                if isinstance(response_list, list):
                    for response in response_list:
                        if 'trigger' in response and response['trigger'].lower().strip() == query_lower:
                            return PredefinedResponse(
                                text=response.get('text', ''),
                                movement=response.get('movement')
                            )
        
        # No matches found - use fallback
        if 'fallbacks' in self.responses and self.responses['fallbacks']:
            fallback = random.choice(self.responses['fallbacks'])
            return PredefinedResponse(
                text=fallback.get('text', ''),
                movement=fallback.get('movement')
            )
        
        return None
    
    def _search_in_category(self, query: str, category_data: Any) -> Optional[Dict]:
        """Search for response in a specific category"""
        if isinstance(category_data, dict):
            # Category has subcategories
            for subcategory in category_data.values():
                if isinstance(subcategory, list):
                    return random.choice(subcategory) if subcategory else None
        elif isinstance(category_data, list):
            # Category is a list of responses
            return random.choice(category_data) if category_data else None
        
        return None
    
    def add_response(self, category: str, subcategory: str, text: str, 
                    movement: str = None, emotion: str = None) -> bool:
        """Add a new predefined response"""
        try:
            if category not in self.responses:
                self.responses[category] = {}
            
            if subcategory not in self.responses[category]:
                self.responses[category][subcategory] = []
            
            new_response = {
                "text": text,
                "movement": movement,
                "emotion": emotion
            }
            
            self.responses[category][subcategory].append(new_response)
            self.save_responses()
            print(f"Added response to {category}/{subcategory}")
            return True
            
        except Exception as e:
            print(f"Error adding response: {e}")
            return False
    
    def remove_response(self, category: str, subcategory: str, index: int) -> bool:
        """Remove a predefined response"""
        try:
            if (category in self.responses and 
                subcategory in self.responses[category] and
                0 <= index < len(self.responses[category][subcategory])):
                
                removed = self.responses[category][subcategory].pop(index)
                self.save_responses()
                print(f"Removed response: {removed['text'][:50]}...")
                return True
            else:
                print(f"Response not found at {category}/{subcategory}[{index}]")
                return False
                
        except Exception as e:
            print(f"Error removing response: {e}")
            return False
    
    def list_responses(self, category: str = None) -> Dict:
        """List all responses or responses in a specific category"""
        if category:
            return self.responses.get(category, {})
        return self.responses
    
    def get_response_count(self) -> int:
        """Get total number of predefined responses"""
        count = 0
        for category in self.responses.values():
            if isinstance(category, dict):
                for subcategory in category.values():
                    if isinstance(subcategory, list):
                        count += len(subcategory)
            elif isinstance(category, list):
                count += len(category)
        return count
    
    def load_settings(self):
        """Load system settings"""
        try:
            settings_file = "worm_settings.json"
            if os.path.exists(settings_file):
                with open(settings_file, 'r') as f:
                    self.settings = json.load(f)
            else:
                self.settings = self._create_default_settings()
                self.save_settings()
                
            print(f"Settings loaded")
        except Exception as e:
            print(f"Error loading settings: {e}")
            self.settings = self._create_default_settings()
    
    def save_settings(self):
        """Save system settings"""
        try:
            with open("worm_settings.json", 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def _create_default_settings(self) -> Dict:
        """Create default settings"""
        return {
            "audio": {
                "volume": 0.8,
                "speech_speed": 150,
                "voice_timeout": 5.0
            },
            "movement": {
                "default_delay": 0.5,
                "animation_speed": 1.0
            },
            "ai": {
                "use_ai_fallback": True,
                "ai_confidence_threshold": 0.6,
                "max_response_length": 200
            },
            "debug": {
                "verbose_logging": False,
                "simulation_mode": False
            }
        }
    
    def get_setting(self, key: str, default=None):
        """Get a setting value using dot notation (e.g., 'audio.volume')"""
        keys = key.split('.')
        value = self.settings
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set_setting(self, key: str, value):
        """Set a setting value using dot notation"""
        keys = key.split('.')
        setting = self.settings
        
        for k in keys[:-1]:
            if k not in setting:
                setting[k] = {}
            setting = setting[k]
        
        setting[keys[-1]] = value
        self.save_settings()
    
    def export_responses(self, filename: str) -> bool:
        """Export responses to a backup file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.responses, f, indent=2, ensure_ascii=False)
            print(f"Responses exported to {filename}")
            return True
        except Exception as e:
            print(f"Export error: {e}")
            return False
    
    def import_responses(self, filename: str) -> bool:
        """Import responses from a backup file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                imported_responses = json.load(f)
            
            self.responses = imported_responses
            self.save_responses()
            print(f"Responses imported from {filename}")
            return True
        except Exception as e:
            print(f"Import error: {e}")
            return False
    
    def get_stats(self) -> Dict:
        """Get statistics about the configuration"""
        return {
            "total_responses": self.get_response_count(),
            "categories": len(self.responses),
            "settings_loaded": len(self.settings) > 0,
            "responses_file": self.responses_file,
            "file_exists": os.path.exists(self.responses_file)
        } 