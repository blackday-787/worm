"""
🎤 WORM AUDIO CONTROLLER  
Pure audio control - no AI dependencies
Handles TTS, voice recognition, and audio playback
"""

import pygame
import time
import threading
from gtts import gTTS
import tempfile
import os
from typing import Optional, Callable
import vosk
import json
import sounddevice as sd
import queue

class AudioController:
    """Pure audio controller for the worm robot"""
    
    def __init__(self):
        self.setup_audio()
        self.vosk_model = None
        self.recognizer = None
        self.vosk_checked = False
        self.is_speaking = False
        self.audio_queue = queue.Queue()
        
    def setup_audio(self):
        """Initialize audio components for voice input/output"""
        try:
            # Initialize pygame for audio playback
            pygame.mixer.init()
            print("Audio playback ready")
        except Exception as e:
            print(f"⚠️  Audio setup failed: {e}")
    
        
    def speak(self, text: str, speed: int = 150, blocking: bool = True):
        """Convert text to speech and play it"""
        if self.is_speaking and blocking:
            return  # Prevent overlapping speech
            
        def _speak():
            self.is_speaking = True
            try:
                # Create TTS with female voice
                tts = gTTS(text=text, lang='en', slow=(speed < 100))
                
                # Save to temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                    tts.save(tmp_file.name)
                    
                    # Play audio
                    pygame.mixer.music.load(tmp_file.name)
                    pygame.mixer.music.play()
                    
                    # Wait for playback to finish
                    while pygame.mixer.music.get_busy():
                        time.sleep(0.1)
                    
                    # Clean up
                    os.unlink(tmp_file.name)
                    
            except Exception as e:
                print(f"❌ Speech error: {e}")
            finally:
                self.is_speaking = False
        
        if blocking:
            _speak()
        else:
            # Run in background thread
            threading.Thread(target=_speak, daemon=True).start()
    
    def is_active(self) -> bool:
        """Check if audio is currently playing"""
        return pygame.mixer.music.get_busy() or self.is_speaking
    
    def setup_voice_recognition(self) -> bool:
        """Setup voice recognition (lazy loading)"""
        if self.vosk_checked:
            return self.vosk_model is not None
            
        self.vosk_checked = True
        
        try:
            # Look for Vosk model
            model_paths = [
                "vosk-model-small-en-us-0.15",
                "model/vosk-model-small-en-us-0.15"
            ]
            
            model_path = None
            for path in model_paths:
                if os.path.exists(path):
                    model_path = path
                    break
            
            if not model_path:
                print("⚠️  Vosk model not found - voice recognition disabled")
                return False
            
            self.vosk_model = vosk.Model(model_path)
            self.recognizer = vosk.KaldiRecognizer(self.vosk_model, 16000)
            print("✅ Voice recognition ready")
            return True
            
        except Exception as e:
            print(f"⚠️  Voice recognition setup failed: {e}")
            return False
    
    def listen_for_speech(self, timeout: float = 5.0, callback: Optional[Callable] = None) -> Optional[str]:
        """Listen for speech input"""
        if not self.setup_voice_recognition():
            return None
        
        print("🎤 Listening...")
        
        try:
            # Audio recording parameters
            sample_rate = 16000
            duration = timeout
            
            # Record audio
            audio_data = sd.rec(int(duration * sample_rate), 
                              samplerate=sample_rate, 
                              channels=1, 
                              dtype='int16')
            sd.wait()  # Wait for recording to complete
            
            # Process with Vosk
            if self.recognizer.AcceptWaveform(audio_data.tobytes()):
                result = json.loads(self.recognizer.Result())
                text = result.get('text', '').strip()
                
                if text:
                    print(f"🎤 Heard: '{text}'")
                    if callback:
                        callback(text)
                    return text
                else:
                    print("🔇 No speech detected")
                    return None
            else:
                print("🔇 Speech recognition failed")
                return None
                
        except Exception as e:
            print(f"❌ Voice recognition error: {e}")
            return None
    
    def start_continuous_listening(self, callback: Callable[[str], None]):
        """Start continuous voice recognition in background"""
        if not self.setup_voice_recognition():
            return False
        
        def _listen_continuously():
            print("🎤 Continuous listening started...")
            
            with sd.InputStream(samplerate=16000, channels=1, dtype='int16',
                              callback=self._audio_callback):
                while True:
                    try:
                        # Process audio queue
                        if not self.audio_queue.empty():
                            audio_chunk = self.audio_queue.get_nowait()
                            
                            if self.recognizer.AcceptWaveform(audio_chunk):
                                result = json.loads(self.recognizer.Result())
                                text = result.get('text', '').strip()
                                
                                if text:
                                    print(f"🎤 Heard: '{text}'")
                                    callback(text)
                        
                        time.sleep(0.1)
                        
                    except KeyboardInterrupt:
                        break
                    except Exception as e:
                        print(f"❌ Continuous listening error: {e}")
                        time.sleep(1)
        
        # Start in background thread
        threading.Thread(target=_listen_continuously, daemon=True).start()
        return True
    
    def _audio_callback(self, indata, frames, time, status):
        """Callback for continuous audio input"""
        if status:
            print(f"Audio input status: {status}")
        
        # Add audio data to queue for processing
        self.audio_queue.put(indata.copy().tobytes())
    
    def stop_audio(self):
        """Stop all audio playback"""
        try:
            pygame.mixer.music.stop()
            self.is_speaking = False
        except Exception as e:
            print(f"❌ Error stopping audio: {e}")
    
    def set_volume(self, volume: float):
        """Set audio volume (0.0 to 1.0)"""
        try:
            pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))
        except Exception as e:
            print(f"❌ Error setting volume: {e}")
    
    def close(self):
        """Clean up audio resources"""
        self.stop_audio()
        pygame.mixer.quit()
        print("🔇 Audio controller closed") 