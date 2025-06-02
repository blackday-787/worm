"""
🐛 WORM SYSTEM - REFACTORED ARCHITECTURE
Main orchestrator that coordinates between AI, hardware, and configuration
"""

import time
import threading
from typing import Optional, Dict
import signal
import sys

# Import our separated modules
from core.worm_controller import WormController
from core.audio_controller import AudioController
from ai.ai_processor import AIProcessor, AIResponse, ResponseType
from config_manager import ConfigManager, PredefinedResponse

class WormSystem:
    """Main worm system orchestrator - coordinates all subsystems"""
    
    def __init__(self):
        print("🐛 WORM SYSTEM STARTING...")
        print("=" * 50)
        
        # Initialize all subsystems
        self.config = ConfigManager()
        self.hardware = WormController()
        self.audio = AudioController()
        self.ai = AIProcessor()
        
        # System state
        self.running = False
        self.listening = False
        self.last_movement_time = 0
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        print("🚀 WORM SYSTEM READY!")
        self._print_system_status()
    
    def _print_system_status(self):
        """Print the status of all subsystems"""
        print("\n📊 SYSTEM STATUS:")
        print(f"🤖 Hardware: {'✅ Connected' if self.hardware.is_connected() else '🤖 Simulation'}")
        print(f"🎤 Audio: ✅ Ready")
        print(f"🧠 AI: {'✅ Ready' if self.ai.is_available() else '❌ Disabled'}")
        print(f"⚙️  Config: ✅ {self.config.get_response_count()} responses loaded")
        print()
    
    def start(self, voice_mode: bool = True):
        """Start the main WORM system"""
        self.running = True
        
        # Welcome message
        self._respond("Hello! I'm WORM, your friendly robot companion! 🐛")
        
        if voice_mode:
            print("🎤 Starting voice interaction mode...")
            print("💡 Say 'worm' to get my attention, or 'quit' to exit")
            self._start_voice_mode()
        else:
            print("💬 Starting text interaction mode...")
            print("💡 Type your messages or 'quit' to exit")
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
            print("👋 Goodbye!")
            self.stop()
    
    def _process_input(self, user_input: str) -> Optional[Dict]:
        """Process user input and generate response"""
        print(f"\n👤 User: {user_input}")
        
        # Try to find a predefined response first
        predefined_response = self.config.find_response(user_input)
        
        if predefined_response and predefined_response.text:
            # Use predefined response
            response_text = predefined_response.text
            movement = predefined_response.movement
            
            print(f"📖 Using predefined response")
            self._respond(response_text, movement)
            
            return {
                "type": "predefined",
                "text": response_text,
                "movement": movement
            }
        
        elif self.ai.is_available():
            # Use AI to generate response
            ai_response = self.ai.generate_response(user_input)
            
            if ai_response and ai_response.text:
                # Determine movement from AI suggestions
                movement = None
                if ai_response.movement_hint:
                    movement = self._map_ai_movement_to_command(ai_response.movement_hint)
                elif ai_response.emotion:
                    movement = self.ai.suggest_emotion_movement(ai_response.emotion)
                
                print(f"🧠 Using AI response (confidence: {ai_response.confidence:.2f})")
                self._respond(ai_response.text, movement)
                
                return {
                    "type": "ai_generated",
                    "text": ai_response.text,
                    "movement": movement,
                    "confidence": ai_response.confidence
                }
        
        # Fallback response
        fallback_response = self.config.find_response("", "fallbacks")
        if fallback_response:
            self._respond(fallback_response.text, fallback_response.movement)
            return {
                "type": "fallback",
                "text": fallback_response.text,
                "movement": fallback_response.movement
            }
        
        # Last resort
        self._respond("I'm not sure how to respond to that, but I'm always learning!")
        return {"type": "error", "text": "No response generated"}
    
    def _respond(self, text: str, movement: str = None):
        """Generate a complete response with speech and movement"""
        print(f"🐛 WORM: {text}")
        
        # Coordinate movement and speech
        if movement:
            self._perform_movement_with_speech(text, movement)
        else:
            # Just speak with default talking animation
            self._perform_movement_with_speech(text, "talk_animation")
    
    def _perform_movement_with_speech(self, text: str, movement: str):
        """Coordinate movement and speech timing"""
        # Start movement
        if hasattr(self.hardware, movement):
            getattr(self.hardware, movement)()
        else:
            # Default to talking animation
            self.hardware.talk_animation()
        
        # Speak the text (non-blocking)
        self.audio.speak(text, blocking=False)
        
        # Update last movement time
        self.last_movement_time = time.time()
    
    def _map_ai_movement_to_command(self, ai_movement: str) -> str:
        """Map AI movement suggestions to hardware commands"""
        movement_mapping = {
            "dance": "dance_animation",
            "wiggle": "talk_animation",
            "move": "choreographed_talk",
            "happy": "dance_animation",
            "sad": "sadness_movement",
            "excited": "dance_animation",
            "talk": "talk_animation",
            "forward": "move_forward_left",
            "back": "move_back_left"
        }
        
        for key, command in movement_mapping.items():
            if key in ai_movement.lower():
                return command
        
        return "talk_animation"  # Default
    
    def manual_command(self, command: str) -> bool:
        """Execute a manual hardware command"""
        if hasattr(self.hardware, command):
            print(f"🤖 Executing: {command}")
            return getattr(self.hardware, command)()
        else:
            print(f"❌ Unknown command: {command}")
            return False
    
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
                "voice_recognition": self.audio.vosk_model is not None
            },
            "ai": {
                "available": self.ai.is_available(),
                "conversation_length": len(self.ai.conversation_history)
            },
            "config": self.config.get_stats(),
            "system": {
                "running": self.running,
                "listening": self.listening
            }
        }
    
    def _signal_handler(self, signum, frame):
        """Handle system signals for graceful shutdown"""
        print(f"\n🛑 Received signal {signum}, shutting down...")
        self.stop()
    
    def stop(self):
        """Stop the WORM system gracefully"""
        print("\n🛑 SHUTTING DOWN WORM SYSTEM...")
        
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
        self.ai.close()
        
        print("👋 WORM system stopped. Goodbye!")

def main():
    """Main entry point"""
    try:
        worm = WormSystem()
        
        # Choose interaction mode
        mode = input("Choose mode - (v)oice or (t)ext [v]: ").lower()
        voice_mode = mode != 't'
        
        worm.start(voice_mode=voice_mode)
        
    except Exception as e:
        print(f"❌ System error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("🔚 Program ended")

if __name__ == "__main__":
    main() 