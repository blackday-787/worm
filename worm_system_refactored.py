"""
WORM SYSTEM - REFACTORED ARCHITECTURE (AI-FREE)
Main orchestrator that coordinates between hardware, audio, and configuration
Text-to-speech and predefined responses remain fully functional
"""

import time
import threading
from typing import Optional, Dict
import signal
import sys
import argparse

# Import our separated modules
from core.worm_controller import WormController
from core.audio_controller import AudioController
from config_manager import ConfigManager, PredefinedResponse

class WormSystem:
    """Main worm system orchestrator - coordinates all subsystems (AI-free)"""
    
    def __init__(self):
        print("WORM SYSTEM STARTING... (AI-FREE MODE)")
        print("=" * 50)
        
        # Initialize all subsystems (no AI)
        self.config = ConfigManager()
        self.hardware = WormController()
        self.audio = AudioController()
        
        # System state
        self.running = False
        self.listening = False
        self.last_movement_time = 0
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        print("WORM SYSTEM READY! (Text-to-Speech & Predefined Responses)")
        self._print_system_status()
    
    def _print_system_status(self):
        """Print the status of all subsystems"""
        print("\nSYSTEM STATUS:")
        print(f"Hardware: {'Connected' if self.hardware.is_connected() else 'Simulation'}")
        print(f"Audio: Ready (TTS Functional)")
        print(f"AI: Removed (Predefined responses only)")
        print(f"Config: {self.config.get_response_count()} responses loaded")
        print("Use response editor to add new responses!")
        print()
    
    def start(self, voice_mode: bool = True):
        """Start the main WORM system"""
        self.running = True
        
        if voice_mode:
            print("Starting voice interaction mode...")
            print("Say 'worm' to get my attention, or 'quit' to exit")
            self._start_voice_mode()
        else:
            print("Starting text interaction mode...")
            print("Type your messages or 'quit' to exit")
            self._start_text_mode()
    
    def _start_voice_mode(self):
        """Start voice interaction mode"""
        self.listening = True
        
        # Start continuous listening
        self.audio.start_continuous_listening(self._handle_voice_input)
        
        try:
            while self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop()
    
    def _start_text_mode(self):
        """Start text interaction mode"""
        try:
            while self.running:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'stop']:
                    break
                
                if user_input:
                    self._process_input(user_input)
        except KeyboardInterrupt:
            pass
        finally:
            self.stop()
    
    def _handle_voice_input(self, text: str):
        """Handle voice input from audio controller"""
        if not self.running:
            return
        
        # Check for wake word or direct commands
        text_lower = text.lower()
        
        if 'worm' in text_lower or any(word in text_lower for word in ['hello', 'hey']):
            # Remove wake word and process
            processed_text = text_lower.replace('worm', '').strip()
            if processed_text:
                self._process_input(processed_text)
            else:
                self._respond("Yes? How can I help you?")
        elif text_lower in ['quit', 'exit', 'stop']:
            print("Goodbye!")
            self.stop()
    
    def _process_input(self, user_input: str) -> Optional[Dict]:
        """Process user input and generate response (AI-free)"""
        print(f"\nUser: {user_input}")
        
        # Check for direct Arduino commands first
        arduino_commands = ["d", "s", "fl", "fr", "bl", "br", "sl", "sr", "w", "b", "om", "cm", "identify"]
        user_lower = user_input.lower().strip()
        
        if user_lower in arduino_commands:
            print(f"Executing Arduino command: {user_lower}")
            success = self.hardware.send_command(user_lower)
            return {
                "type": "direct_command",
                "command": user_lower,
                "success": success
            }
        
        # Try to find a predefined response
        predefined_response = self.config.find_response(user_input)
        
        if predefined_response and predefined_response.text:
            # Use predefined response
            response_text = predefined_response.text
            movement = predefined_response.movement
            
            print(f"Using predefined response")
            self._respond(response_text, movement)
            
            return {
                "type": "predefined",
                "text": response_text,
                "movement": movement
            }
        
        # Enhanced fallback with better response matching
        fallback_response = self._find_enhanced_fallback(user_input)
        if fallback_response:
            self._respond(fallback_response.text, fallback_response.movement)
            return {
                "type": "fallback",
                "text": fallback_response.text,
                "movement": fallback_response.movement
            }
        
        # Last resort
        default_text = "I'm not sure how to respond to that, but I'm always learning! Try asking about dancing, moving, or saying hello!"
        self._respond(default_text)
        return {"type": "error", "text": default_text}
    
    def _find_enhanced_fallback(self, user_input: str) -> Optional[PredefinedResponse]:
        """Find a better fallback response based on keywords"""
        user_lower = user_input.lower()
        
        # Simple keyword matching for fallbacks (no movement mapping)
        if any(word in user_lower for word in ['dance', 'move', 'wiggle', 'motion']):
            return self.config.find_response("dance", "commands")
        elif any(word in user_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return self.config.find_response("hello", "greetings")
        elif any(word in user_lower for word in ['what', 'who', 'how', 'why']):
            return self.config.find_response("what are you", "questions")
        elif any(word in user_lower for word in ['happy', 'good', 'great', 'awesome']):
            return self.config.find_response("", "emotions")
        else:
            # Use standard fallback
            return self.config.find_response("", "fallbacks")
    
    def _respond(self, text: str, movement: str = None):
        """Generate a complete response with speech and movement"""
        print(f"WORM: {text}")
        
        # Coordinate movement and speech
        if movement:
            self._perform_movement_with_speech(text, movement)
        else:
            # Just speak without movement
            self.audio.speak(text, blocking=False)
    
    def _perform_movement_with_speech(self, text: str, movement: str):
        """Coordinate movement and speech timing"""
        # Send movement command directly to Arduino
        if movement:
            self.hardware.send_command(movement)
        
        # Speak the text (non-blocking)
        self.audio.speak(text, blocking=False)
        
        # Update last movement time
        self.last_movement_time = time.time()
    
    def manual_command(self, command: str) -> bool:
        """Execute a manual hardware command (direct Arduino shortcuts)"""
        print(f"Executing: {command}")
        return self.hardware.send_command(command)
    
    def add_response(self, category: str, subcategory: str, text: str, movement: str = None):
        """Add a new predefined response"""
        return self.config.add_response(category, subcategory, text, movement)
    
    def list_responses(self, category: str = None):
        """List available responses"""
        return self.config.list_responses(category)
    
    def get_system_stats(self) -> Dict:
        """Get comprehensive system statistics"""
        return {
            "hardware": {
                "connected": self.hardware.is_connected(),
                "last_movement": self.last_movement_time
            },
            "audio": {
                "is_speaking": self.audio.is_speaking,
                "voice_recognition": self.audio.vosk_model is not None,
                "tts_functional": True
            },
            "ai": {
                "available": False,
                "status": "removed"
            },
            "config": self.config.get_stats(),
            "system": {
                "running": self.running,
                "listening": self.listening,
                "mode": "ai_free"
            }
        }
    
    def _signal_handler(self, signum, frame):
        """Handle system signals for graceful shutdown"""
        print(f"\nReceived signal {signum}, shutting down...")
        self.stop()
    
    def stop(self):
        """Stop the WORM system gracefully"""
        print("\nSHUTTING DOWN WORM SYSTEM...")
        
        self.running = False
        self.listening = False
        
        # Stop audio
        self.audio.stop_audio()
        
        # Reset hardware position
        if self.hardware.is_connected():
            self.hardware.reset_position()
        
        # Close all subsystems
        self.hardware.close()
        self.audio.close()
        
        print("WORM system stopped. Goodbye!")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="WORM Robot System (AI-Free)")
    parser.add_argument('--voice', action='store_true', help='Start in voice mode')
    parser.add_argument('--text', action='store_true', help='Start in text mode')
    
    args = parser.parse_args()
    
    try:
        worm = WormSystem()
        
        # Determine interaction mode
        if args.voice:
            voice_mode = True
            print("Starting in voice mode (from command line)")
        elif args.text:
            voice_mode = False
            print("Starting in text mode (from command line)")
        else:
            # Interactive mode selection
            mode = input("Choose mode - (v)oice or (t)ext [v]: ").lower()
            voice_mode = mode != 't'
        
        worm.start(voice_mode=voice_mode)
        
    except Exception as e:
        print(f"System error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Program ended")

if __name__ == "__main__":
    main() 