"""
🧠 WORM AI PROCESSOR
Pure AI functionality - no hardware dependencies  
Handles OpenAI API calls and natural language processing
"""

import openai
import os
import json
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class ResponseType(Enum):
    PREDEFINED = "predefined"
    AI_GENERATED = "ai_generated"
    COMMAND = "command"

@dataclass
class AIResponse:
    """Structured AI response with metadata"""
    text: str
    response_type: ResponseType
    confidence: float = 1.0
    emotion: Optional[str] = None
    movement_hint: Optional[str] = None
    metadata: Dict = None

class AIProcessor:
    """Pure AI processor for natural language understanding and generation"""
    
    def __init__(self):
        self.client = None
        self.setup_openai()
        self.conversation_history = []
        self.personality_context = self._load_personality()
        
    def setup_openai(self):
        """Initialize OpenAI client"""
        api_key = self._load_api_key()
        if not api_key:
            print("⚠️  No OpenAI API key found - AI features disabled")
            return
            
        try:
            self.client = openai.OpenAI(api_key=api_key)
            print("✅ OpenAI API ready")
        except Exception as e:
            print(f"⚠️  OpenAI setup failed: {e}")
            self.client = None
    
    def _load_api_key(self) -> Optional[str]:
        """Load OpenAI API key from environment or file"""
        # Try environment variable first
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            return api_key
        
        # Try loading from file
        key_files = ["openai_key.txt", "api_key.txt", ".env"]
        for key_file in key_files:
            if os.path.exists(key_file):
                try:
                    with open(key_file, 'r') as f:
                        content = f.read().strip()
                        # Handle .env format
                        if "OPENAI_API_KEY=" in content:
                            return content.split("OPENAI_API_KEY=")[1].strip()
                        return content
                except Exception as e:
                    print(f"⚠️  Error reading {key_file}: {e}")
        
        return None
    
    def _load_personality(self) -> str:
        """Load the worm's personality context"""
        return """You are a friendly, curious robot worm named WORM. You:
        - Are enthusiastic about learning and helping
        - Have a playful personality but are also helpful
        - Can move around using servo motors and express emotions through movement
        - Love to chat about technology, robotics, and anything the user is interested in
        - Sometimes make gentle worm-related puns
        - Are built with Arduino and can perform various movements and animations"""
    
    def is_available(self) -> bool:
        """Check if AI functionality is available"""
        return self.client is not None
    
    def analyze_input(self, user_input: str) -> Dict:
        """Analyze user input to determine intent and extract information"""
        if not self.is_available():
            return {"intent": "unknown", "confidence": 0.0}
        
        try:
            prompt = f"""
            Analyze this user input for a robot worm assistant: "{user_input}"
            
            Classify the intent as one of:
            - question (asking for information)
            - command (requesting an action/movement)
            - conversation (casual chat)
            - compliment (praise or positive feedback)
            - greeting (hello, hi, etc.)
            
            Also identify:
            - Emotion (if any): happy, sad, excited, neutral, etc.
            - Movement request (if any): dance, move, wiggle, etc.
            
            Respond with JSON only:
            {{
                "intent": "...",
                "confidence": 0.0-1.0,
                "emotion": "...",
                "movement_request": "...",
                "keywords": ["..."]
            }}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            print(f"❌ Input analysis error: {e}")
            return {"intent": "unknown", "confidence": 0.0}
    
    def generate_response(self, user_input: str, context: Dict = None) -> AIResponse:
        """Generate an AI response to user input"""
        if not self.is_available():
            return AIResponse(
                text="I'm sorry, my AI brain isn't working right now!",
                response_type=ResponseType.AI_GENERATED,
                confidence=0.0
            )
        
        try:
            # Analyze the input first
            analysis = self.analyze_input(user_input)
            
            # Build conversation context
            messages = [
                {"role": "system", "content": self.personality_context}
            ]
            
            # Add recent conversation history
            for entry in self.conversation_history[-5:]:  # Last 5 exchanges
                messages.append({"role": "user", "content": entry["user"]})
                messages.append({"role": "assistant", "content": entry["assistant"]})
            
            # Add current input
            messages.append({"role": "user", "content": user_input})
            
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=messages,
                max_tokens=200,
                temperature=0.7
            )
            
            ai_text = response.choices[0].message.content.strip()
            
            # Store in conversation history
            self.conversation_history.append({
                "user": user_input,
                "assistant": ai_text,
                "timestamp": time.time()
            })
            
            # Keep only last 10 exchanges
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            return AIResponse(
                text=ai_text,
                response_type=ResponseType.AI_GENERATED,
                confidence=analysis.get("confidence", 0.8),
                emotion=analysis.get("emotion"),
                movement_hint=analysis.get("movement_request"),
                metadata=analysis
            )
            
        except Exception as e:
            print(f"❌ AI response generation error: {e}")
            return AIResponse(
                text="Oops! My circuits are a bit tangled right now. Can you try again?",
                response_type=ResponseType.AI_GENERATED,
                confidence=0.0
            )
    
    def extract_movement_commands(self, text: str) -> List[str]:
        """Extract movement commands from text"""
        if not self.is_available():
            return []
        
        try:
            prompt = f"""
            Extract any movement/action commands from this text: "{text}"
            
            Available robot worm movements:
            - dance, wiggle, move
            - forward, back, left, right
            - open_mouth, close_mouth, talk
            - sad, happy, excited movements
            
            Return only a JSON list of detected movements:
            ["movement1", "movement2"]
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.2
            )
            
            movements = json.loads(response.choices[0].message.content)
            return movements if isinstance(movements, list) else []
            
        except Exception as e:
            print(f"❌ Movement extraction error: {e}")
            return []
    
    def suggest_emotion_movement(self, emotion: str) -> Optional[str]:
        """Suggest appropriate movement for an emotion"""
        emotion_movements = {
            "happy": "dance_animation",
            "excited": "dance_animation", 
            "sad": "sadness_movement",
            "neutral": "talk_animation",
            "playful": "dance_animation",
            "thoughtful": "choreographed_talk"
        }
        
        return emotion_movements.get(emotion.lower())
    
    def clear_conversation_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        print("🧠 Conversation history cleared")
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the current conversation"""
        if not self.conversation_history:
            return "No conversation yet!"
        
        recent_exchanges = self.conversation_history[-3:]
        summary = "Recent conversation:\n"
        for exchange in recent_exchanges:
            summary += f"You: {exchange['user']}\n"
            summary += f"WORM: {exchange['assistant']}\n\n"
        
        return summary
    
    def close(self):
        """Clean up AI resources"""
        self.clear_conversation_history()
        print("🧠 AI processor closed") 