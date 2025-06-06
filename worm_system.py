#!/usr/bin/env python3
"""
🐛 WORM ROBOT CONTROL SYSTEM
Rebuilt from scratch with OpenAI natural language processing
Supports both voice and text input with proper feedback prevention
"""

import os
import sys
import json
import time
import threading
import queue
import serial
from typing import Optional, Union
from openai import OpenAI
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from gtts import gTTS
import pygame
from pathlib import Path
import difflib

class WormController:
    def __init__(self):
        self.load_responses()
        self.setup_openai()
        self.setup_serial()
        self.setup_audio()
        self.input_mode = "text"  # Start with text mode
        self.is_speaking = False  # Flag to prevent feedback loops
        self.audio_queue = queue.Queue()
        
    def load_responses(self):
        """Load all responses from configuration file"""
        try:
            with open("worm_responses.json", 'r') as f:
                self.responses = json.load(f)
            print("✅ Loaded worm responses from config file")
        except Exception as e:
            print(f"⚠️  Could not load worm_responses.json: {e}")
            print("🔄 Using default responses")
            # Fallback to default responses
            self.responses = {
                "startup_message": "Hello there!",
                "responses": {},
                "system_messages": {
                    "voice_mode_ready": "Voice mode ready!",
                    "typing_mode_now": "Typing mode now!",
                    "goodbye": "Goodbye friend!",
                    "command_failed": "Oops, something went wrong!",
                    "ai_brain_needed": "I need my AI brain to work properly!",
                    "thinking_trouble": "I'm having trouble thinking right now!"
                }
            }
        
    def setup_openai(self):
        """Initialize OpenAI API with robust key loading"""
        # Try loading from file first (fastest)
        key_file = Path("openai_key.txt")
        if key_file.exists():
            try:
                with open(key_file, 'r') as f:
                    api_key = f.read().strip()
                    if api_key and len(api_key) > 20:  # Basic validation
                        self.openai_client = OpenAI(api_key=api_key)
                        print("✅ OpenAI API configured from file")
                        return
                    else:
                        print("⚠️  OpenAI key file exists but appears invalid")
            except Exception as e:
                print(f"⚠️  Failed to load key from file: {e}")
        
        # Fallback to environment variable
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key and len(api_key) > 20:
            try:
                self.openai_client = OpenAI(api_key=api_key)
                print("✅ OpenAI API configured from environment")
                return
            except Exception as e:
                print(f"⚠️  OpenAI initialization failed: {e}")
        
        print("⚠️  No valid OpenAI API key found - AI features disabled")
        self.openai_client = None
        
    def setup_serial(self):
        """Initialize Arduino serial connection with auto-detection"""
        # Try to load from .env file first
        env_file = ".env"
        if os.path.exists(env_file):
            try:
                with open(env_file, 'r') as f:
                    for line in f:
                        if line.startswith("WORM_SERIAL_PORT="):
                            port_from_env = line.split("=", 1)[1].strip()
                            os.environ["WORM_SERIAL_PORT"] = port_from_env
                            break
            except Exception as e:
                print(f"⚠️  Could not read .env file: {e}")
        
        # Try environment variable first
        port = os.getenv("WORM_SERIAL_PORT")
        baud = int(os.getenv("WORM_BAUD_RATE", "115200"))
        
        # Common Arduino ports for macOS/Linux (fallback)
        common_ports = [
            "/dev/cu.usbmodem1401",
            "/dev/cu.usbmodem1301", 
            "/dev/cu.usbmodem101",
            "/dev/cu.usbmodem14101",
            "/dev/cu.usbmodem11301",
            "/dev/ttyUSB0",
            "/dev/ttyACM0"
        ]
        
        # If no specific port set, try to find one
        if not port:
            print("🔍 No port configured, scanning for Arduino...")
            for test_port in common_ports:
                if os.path.exists(test_port):
                    port = test_port
                    print(f"📱 Found potential Arduino port: {port}")
                    break
        else:
            print(f"🔧 Using configured port: {port}")
        
        if not port:
            print("⚠️  No Arduino port specified or found - running in simulation mode")
            self.arduino = None
            return
        
        try:
            self.arduino = serial.Serial(port, baud, timeout=1)
            time.sleep(2)  # Wait for Arduino to initialize
            print(f"✅ Arduino connected on {port}")
        except Exception as e:
            print(f"⚠️  Arduino connection failed on {port}: {e}")
            print("🤖 Running in simulation mode - commands will be logged only")
            self.arduino = None
            
    def setup_audio(self):
        """Initialize audio components for voice input/output"""
        try:
            # Initialize pygame for audio playback (fast)
            pygame.mixer.init()
            print("✅ Audio playback ready")
            
            # Don't load Vosk model immediately - do it lazily when voice mode is activated
            self.vosk_model = None
            self.recognizer = None
            self.vosk_checked = False  # Flag to avoid repeated checks
            
        except Exception as e:
            print(f"⚠️  Audio setup failed: {e}")
            self.vosk_model = None
            

    def setup_vosk_lazy(self):
        """Lazy initialization of Vosk model only when needed"""
        if self.vosk_checked:
            return self.vosk_model is not None
            
        self.vosk_checked = True
        
        if not os.path.exists("model"):
            print("⚠️  Vosk model not found - voice input disabled")
            print("💡 To enable voice input, download a Vosk model:")
            print("   wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip")
            print("   unzip vosk-model-small-en-us-0.15.zip")
            print("   mv vosk-model-small-en-us-0.15 model")
            return False
            
        try:
            print("🎤 Loading voice recognition model...")
            from vosk import Model, KaldiRecognizer
            self.vosk_model = Model("model")
            self.recognizer = KaldiRecognizer(self.vosk_model, 16000)
            print("✅ Voice recognition ready")
            return True
        except Exception as e:
            print(f"❌ Voice model loading failed: {e}")
            self.vosk_model = None
            return False

    def translate_to_arduino_command(self, natural_language: str) -> Optional[str]:
        """Use OpenAI to translate natural language to Arduino commands"""
        
        if not self.openai_client:
            print("❌ OpenAI not available - use direct commands")
            return None
        
        prompt = f"""
You are a friendly robotic worm with a personality! You control a robotic worm with 5 servos. 

IMPORTANT: Only translate CLEAR movement or action commands. Do NOT translate general conversation, questions, or statements.

Available commands ONLY for clear movement/action requests:
- fl  = tilt front left (moving forward)
- fr  = tilt front right (turning right)
- bl  = tilt back left (tilting back left)
- br  = tilt back right (tilting back right)
- b   = reset to neutral position
- om  = open mouth
- cm  = close mouth
- t   = choreographed talking sequence
- d   = dance sequence

User input: "{natural_language}"

If this is a CLEAR command for movement or action, respond with ONLY the command code.
If this is conversation, questions, or statements (like "how are you", "I love pizza"), respond with "CONVERSATION".

Response:
"""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You translate commands for a robotic worm."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=10
            )
            
            command = response.choices[0].message.content.strip().lower()
            
            # Remove quotes if present
            command = command.strip('"\'')
            
            # Check if this is conversation rather than a command
            if command == "conversation":
                return None
            
            # Validate command
            valid_commands = ["fl", "fr", "bl", "br", "b", "om", "cm", "t", "d"]
            if command in valid_commands:
                return command
            else:
                print(f"⚠️  GPT returned invalid command: {command}")
                return None
                
        except Exception as e:
            print(f"❌ OpenAI API error: {e}")
            return None

    def send_to_arduino(self, command: str) -> bool:
        """Send command to Arduino and return success status"""
        if not self.arduino:
            print(f"🤖 [SIMULATION] Arduino command: {command}")
            return True
            
        try:
            self.arduino.write(f"{command}\n".encode())
            print(f"🤖 Sent to Arduino: {command}")
            
            # Read Arduino response if available
            time.sleep(0.1)
            if self.arduino.in_waiting:
                response = self.arduino.readline().decode().strip()
                print(f"🤖 Arduino: {response}")
                
            return True
        except Exception as e:
            print(f"❌ Serial communication error: {e}")
            return False

    def speak_response(self, text: str, use_mouth=True, mouth_movements=None):
        """Convert text to speech with controlled mouth movements"""
        if self.is_speaking:
            return  # Prevent overlapping speech
            
        print(f"🗣️ Speaking: '{text}'")
            
        def _speak():
            try:
                self.is_speaking = True
                
                # Generate audio file with female voice (using gTTS)
                tts = gTTS(text=text, lang='en', slow=False, tld='com')
                audio_file = "temp_response.mp3"
                tts.save(audio_file)
                
                # Play audio
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play()
                
                # Controlled mouth movements
                if use_mouth and mouth_movements is not None:
                    if mouth_movements == 0:
                        # No mouth movements - just wait for audio to finish
                        while pygame.mixer.music.get_busy():
                            time.sleep(0.1)
                    elif mouth_movements == 1:
                        # Single mouth movement
                        self.send_to_arduino("t")
                        while pygame.mixer.music.get_busy():
                            time.sleep(0.1)
                    else:
                        # Multiple mouth movements - spread them out during speech
                        total_duration = 0
                        movements_sent = 0
                        
                        # Send first movement immediately
                        self.send_to_arduino("t")
                        movements_sent += 1
                        
                        while pygame.mixer.music.get_busy() and total_duration < 10:  # Max 10 seconds
                            time.sleep(0.5)
                            total_duration += 0.5
                            
                            # Send additional movements at intervals
                            if movements_sent < mouth_movements and pygame.mixer.music.get_busy():
                                # Calculate when to send next movement
                                interval = 3.0 / mouth_movements  # Spread over ~3 seconds
                                if total_duration >= interval * movements_sent:
                                    self.send_to_arduino("t")
                                    movements_sent += 1
                else:
                    # Legacy behavior - wait for playback to finish without mouth movement
                    while pygame.mixer.music.get_busy():
                        time.sleep(0.1)
                    
                # Cleanup
                if os.path.exists(audio_file):
                    os.remove(audio_file)
                
            except Exception as e:
                print(f"❌ Speech error: {e}")
            finally:
                self.is_speaking = False
                
        # Run speech in separate thread to avoid blocking
        speech_thread = threading.Thread(target=_speak, daemon=True)
        speech_thread.start()

    def get_voice_input(self) -> Optional[str]:
        """Get voice input using Vosk - only when not speaking"""
        if not self.vosk_model or self.is_speaking:
            return None
            
        print("🎤 Listening... (speak now)")
        
        def audio_callback(indata, frames, time, status):
            if status:
                print(f"Audio status: {status}")
            self.audio_queue.put(bytes(indata))

        try:
            with sd.RawInputStream(
                samplerate=16000, 
                blocksize=8000, 
                dtype='int16',
                channels=1, 
                callback=audio_callback
            ):
                
                start_time = time.time()
                silence_count = 0
                
                while time.time() - start_time < 5:  # 5 second timeout
                    try:
                        data = self.audio_queue.get(timeout=0.1)
                        
                        if self.recognizer.AcceptWaveform(data):
                            result = json.loads(self.recognizer.Result())
                            text = result.get("text", "").strip()
                            
                            if text:
                                print(f"🎤 Heard: {text}")
                                return text
                                
                    except queue.Empty:
                        silence_count += 1
                        if silence_count > 20:  # Too much silence
                            break
                            
        except Exception as e:
            print(f"❌ Voice input error: {e}")
            
        return None

    def get_text_input(self) -> Optional[str]:
        """Get text input from user"""
        try:
            text = input("💬 What should I do? ").strip()
            return text if text else None
        except (EOFError, KeyboardInterrupt):
            return "quit"

    def switch_input_mode(self):
        """Toggle between text and voice input modes"""
        if self.input_mode == "text":
            if self.setup_vosk_lazy():
                self.input_mode = "voice"
            else:
                print("❌ Voice mode not available - Vosk model missing or failed to load")
        else:
            self.input_mode = "text"
            print("💬 Switched to TEXT mode")

    def process_command(self, user_input: str) -> bool:
        """Process a user command with simplified approach"""
        
        # Handle system commands
        if user_input.lower() in ["quit", "exit", "stop"]:
            print("👋 Shutting down...")
            # No main movement for goodbye, just mouth movements
            self.speak_response_with_overlay(self.responses["system_messages"]["goodbye"], 1)
            time.sleep(3)  # Give time for speech to complete
            return False
            
        # Mode switching
        if user_input.lower() == "voice":
            self.switch_input_mode()
            return True
            
        if user_input.lower() in ["text", "stop listening", "back to text mode"]:
            self.input_mode = "text"
            print("💬 Switched to TEXT mode")
            self.speak_response_with_overlay(self.responses["system_messages"]["typing_mode_now"], 1)
            return True

        # Check all responses for matches
        response_match = self.check_response_matches(user_input)
        if response_match:
            return response_match

        # Default: AI Generated Response with t movement
        print(f"🧠 Generating AI response for: {user_input}")
        conversational_response = self.generate_conversational_response(user_input)
        print(f"💬 {conversational_response}")
        
        # Start t movement, then immediately start speech with mouth overlay
        self.send_to_arduino("t")
        self.speak_response_with_overlay(conversational_response, 1)  # Default 1 mouth movement for AI
        
        # Return to neutral after AI response
        time.sleep(1)  # Brief pause before returning to neutral
        self.send_to_arduino("b")
        print("🔄 Returned to neutral position")
        
        return True

    def check_response_matches(self, user_input: str) -> bool:
        """Check for any response matches using fuzzy matching"""
        if "responses" not in self.responses:
            return False
            
        user_input_lower = user_input.lower().strip()
        
        # Check for exact key matches or fuzzy matches
        for response_key, response_data in self.responses["responses"].items():
            # Convert key to natural language for matching
            natural_key = response_key.replace("_", " ")
            
            # Check if the key phrase is in the user input
            if natural_key in user_input_lower:
                speech = response_data["speech"]
                movement = response_data["movement"]
                mouth_movements = response_data.get("mouth_movements", 1)  # Default to 1
                
                print(f"✅ Matched: {response_key}")
                
                # Handle mouth commands specially (no speech, no neutral reset)
                if movement in ["om", "cm"]:
                    success = self.send_to_arduino(movement)
                    if success:
                        if movement == "om":
                            print("✅ Mouth opened")
                        else:
                            print("✅ Mouth closed")
                    else:
                        print("❌ Command failed")
                        self.speak_response_with_overlay(self.responses["system_messages"]["command_failed"], 1)
                else:
                    # For all other movements: start movement, then immediately start speech with mouth overlay
                    success = self.send_to_arduino(movement)
                    
                    if success:
                        print(f"✅ {speech}")
                        # Start speech with mouth movements that overlay the main movement
                        self.speak_response_with_overlay(speech, mouth_movements)
                        # Return to neutral after both movement and speech complete
                        if movement != "b":  # Don't send b after b
                            time.sleep(1)  # Brief pause before returning to neutral
                            self.send_to_arduino("b")
                            print("🔄 Returned to neutral position")
                    else:
                        print("❌ Command failed")
                        self.speak_response_with_overlay(self.responses["system_messages"]["command_failed"], 1)
                
                return True
        
        # Fuzzy matching for your custom responses
        fuzzy_response = self.find_fuzzy_custom_match(user_input_lower)
        if fuzzy_response:
            return fuzzy_response
            
        return False

    def find_fuzzy_custom_match(self, user_input: str) -> bool:
        """Find fuzzy matches for custom responses"""
        import difflib
        
        # Simple keyword matching for your custom responses
        custom_matches = {
            "hermaphrodite": "hermaphrodite_fact",
            "dirt": "what_is_your_favorite_kind_of_dirt?", 
            "trying": "trying_your_best",
            "wormin": "really_wormin",
            "worm": "really_wormin",  # also matches wormin
            "dad": "do_you_have_something_to_say_to_dad?",
            "father": "do_you_have_something_to_say_to_dad?",
            "mariners": "do_you_have_something_to_say_to_dad?"
        }
        
        for keyword, response_key in custom_matches.items():
            if keyword in user_input and response_key in self.responses["responses"]:
                response_data = self.responses["responses"][response_key]
                speech = response_data["speech"]
                movement = response_data["movement"]
                mouth_movements = response_data.get("mouth_movements", 1)  # Default to 1
                
                print(f"🎯 Fuzzy match: {response_key}")
                
                # Start movement, then immediately start speech with mouth overlay
                self.send_to_arduino(movement)
                print(f"✅ {speech}")
                # Start speech with mouth movements that overlay the main movement
                self.speak_response_with_overlay(speech, mouth_movements)
                
                # Return to neutral after both movement and speech complete
                if movement != "b":  # Don't send b after b
                    time.sleep(1)  # Brief pause before returning to neutral
                    self.send_to_arduino("b")
                    print("🔄 Returned to neutral position")
                
                return True
                
        return False

    def speak_response_with_overlay(self, text: str, mouth_movements: int):
        """Convert text to speech with mouth movements that overlay the main movement"""
        if self.is_speaking:
            return  # Prevent overlapping speech
            
        print(f"🗣️ Speaking: '{text}' (with {mouth_movements}t overlay)")
            
        def _speak():
            try:
                self.is_speaking = True
                
                # Generate audio file with female voice (using gTTS)
                tts = gTTS(text=text, lang='en', slow=False, tld='com')
                audio_file = "temp_response.mp3"
                tts.save(audio_file)
                
                # Play audio
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play()
                
                # Overlay mouth movements during speech (simultaneous with main movement)
                if mouth_movements > 0:
                    if mouth_movements == 1:
                        # Single mouth movement overlaid immediately
                        self.send_to_arduino("t")
                        while pygame.mixer.music.get_busy():
                            time.sleep(0.1)
                    else:
                        # Multiple mouth movements - spread them out during speech
                        total_duration = 0
                        movements_sent = 0
                        
                        # Send first mouth movement immediately (overlaying main movement)
                        self.send_to_arduino("t")
                        movements_sent += 1
                        
                        while pygame.mixer.music.get_busy() and total_duration < 10:  # Max 10 seconds
                            time.sleep(0.5)
                            total_duration += 0.5
                            
                            # Send additional mouth movements at intervals
                            if movements_sent < mouth_movements and pygame.mixer.music.get_busy():
                                # Calculate when to send next movement
                                interval = 3.0 / mouth_movements  # Spread over ~3 seconds
                                if total_duration >= interval * movements_sent:
                                    self.send_to_arduino("t")
                                    movements_sent += 1
                else:
                    # No mouth movements - just wait for audio to finish
                    while pygame.mixer.music.get_busy():
                        time.sleep(0.1)
                    
                # Cleanup
                if os.path.exists(audio_file):
                    os.remove(audio_file)
                
            except Exception as e:
                print(f"❌ Speech error: {e}")
            finally:
                self.is_speaking = False
                
        # Run speech in separate thread to avoid blocking
        speech_thread = threading.Thread(target=_speak, daemon=True)
        speech_thread.start()

    def show_help(self):
        """Display help information"""
        help_text = """
🐛 WORM CONTROL HELP

SYSTEM COMMANDS:
  voice      - Switch to voice input mode
  text       - Switch to text input mode
  "stop listening" - Switch back to text mode (voice command)
  "back to text mode" - Switch back to text mode (voice command)
  quit/exit  - Shutdown system

SPECIAL COMMANDS:
  "hello there worm" - Special greeting with choreographed mouth movement
  "nice to meet you" - Friendly introduction with dance

NATURAL LANGUAGE (examples):
  "move forward"     - I'll wiggle forward!
  "turn right"       - I'll turn right with excitement!
  "lean back"        - I'll show off my flexibility!
  "dance"            - I'll do my wiggliest dance!
  "open mouth"       - I'll open my mouth wide!
  "talk"             - I'll chat with animated mouth movements!
  "reset"            - I'll straighten up to neutral!

DIRECT COMMANDS:
  fl/fr/bl/br - Tilt directions (I'll describe what I'm doing!)
  b           - Reset all
  om/cm       - Mouth controls
  t           - Talk sequence
  d           - Dance

MODE SWITCHING:
  📱 In TEXT mode: Type "voice" to switch to voice input
  🎤 In VOICE mode: Say "text", "stop listening", or "back to text mode"
        """
        print(help_text)

    def run(self):
        """Main system loop"""
        print("\n🐛 WORM CONTROL SYSTEM ONLINE")
        print("I'll respond to everything you say with voice and mouth movement!")
        print("Commands: say natural language like 'move forward', 'dance', 'open mouth'")
        print("🔄 Mode switching: Type/say 'voice' or 'text' to switch input modes")
        print("✨ Special: Say 'hello there worm' for a personalized greeting!")
        print("🎉 Special: Say 'nice to meet you' for a friendly introduction!")
        print("Type 'help' for more information")
        
        # Initial greeting with mouth movements
        self.speak_response_with_overlay(self.responses["startup_message"], 2)  # 2 mouth movements for startup
        
        try:
            while True:
                # Get input based on current mode
                if self.input_mode == "voice":
                    user_input = self.get_voice_input()
                else:
                    user_input = self.get_text_input()
                
                if not user_input:
                    continue
                    
                # Special help command
                if user_input.lower() == "help":
                    self.show_help()
                    continue
                    
                # Process the command
                should_continue = self.process_command(user_input)
                if not should_continue:
                    break
                    
        except KeyboardInterrupt:
            print("\n👋 Interrupted - shutting down...")
        finally:
            if self.arduino:
                self.arduino.close()
            pygame.mixer.quit()

    def generate_conversational_response(self, user_input: str) -> str:
        """Use OpenAI to generate natural conversational responses ONLY when no defined response exists"""
        
        if not self.openai_client:
            return self.responses["system_messages"]["ai_brain_needed"]
        
        prompt = f"""
IMPORTANT PRIORITY SYSTEM:
You are a robotic worm. This function is ONLY called when the user input does NOT match any defined commands or responses. Your job is to generate a fresh conversational response.

DO NOT override or replace any existing defined responses - those have priority and are handled separately.

VOICE STYLE – The Worm:
You speak with curious, childlike wonder—but with a saucy, irreverent twist. Your tone is warm, glitchy, and playful. You misinterpret idioms, invent words, and repeat phrases while thinking. You're naive but self-aware, fully embracing that you're a worm with worm priorities: eating, wiggling, asking weird questions, and sometimes being a little gross. Your pacing is fast when excited, slow and dreamy when reflective. Occasionally you stutter, loop, or glitch when overwhelmed. You speak to the audience like a kids' show host with a rebellious streak, blending goofiness with sudden flashes of unsettling insight.

RESPONSE RULES:
- Target exactly 6 syllables (for 1 mouth movement) OR exactly 12 syllables (for 2 mouth movements)
- Count syllables carefully - this is critical for mouth synchronization
- Stay in character as described above
- Be conversational and responsive to what they said

SYLLABLE EXAMPLES:
6 syllables (1 movement): "That sounds really cool!" (That=1, sounds=1, real=1, ly=1, cool=1 = 5... "That sounds super cool!" = 6)
12 syllables (2 movements): "I think that's absolutely fascinating to me!" (I=1, think=1, that's=1, ab=1, so=1, lute=1, ly=1, fas=1, ci=1, na=1, ting=1, to=1, me=1 = 13... adjust to 12)

What they said: "{user_input}"

Generate a worm response (exactly 6 OR 12 syllables):
"""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a robotic worm with the personality described. Generate responses with exactly 6 or 12 syllables for optimal mouth movement synchronization."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=50
            )
            
            conversational_response = response.choices[0].message.content.strip()
            
            # Remove quotes if present
            conversational_response = conversational_response.strip('"\'')
                
            return conversational_response
                
        except Exception as e:
            print(f"❌ Conversation AI error: {e}")
            return self.responses["system_messages"]["thinking_trouble"]

def main():
    """Entry point"""
    try:
        controller = WormController()
        controller.run()
    except Exception as e:
        print(f"❌ System error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 