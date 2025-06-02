# 🐛 WORM Robot System - Refactored Architecture

A modular Arduino-based robot worm with AI conversation capabilities, speech synthesis, and movement coordination.

## 🏗️ **Architecture Overview**

The system has been refactored into **3 separate layers** for better maintainability and modularity:

### **1. Core Layer** (No AI dependencies)
```
core/
├── worm_controller.py     # Pure Arduino/servo control
├── audio_controller.py    # TTS, voice recognition, audio playback
└── __init__.py
```

### **2. AI Layer** (No hardware dependencies) 
```
ai/
├── ai_processor.py        # OpenAI API calls, NLP
└── __init__.py
```

### **3. Configuration Layer** (No dependencies)
```
config_manager.py          # Response JSON, settings management
```

### **4. Application Layer** (Orchestration)
```
worm_system_refactored.py  # Main orchestrator
```

## 🚀 **Quick Start**

### **1. Install Dependencies**
```bash
pip install openai pygame gtts vosk sounddevice pyserial
```

### **2. Setup Hardware**
- Connect your Arduino worm robot via USB
- Update the serial port in environment variables if needed:
```bash
export WORM_SERIAL_PORT="/dev/cu.usbmodem1401"
export WORM_BAUD_RATE="115200"
```

### **3. Add OpenAI API Key**
Create `openai_key.txt` with your API key:
```
sk-your-openai-api-key-here
```

### **4. Run the System**
```bash
python worm_system_refactored.py
```

## 🎮 **Usage Modes**

### **Voice Mode** (Default)
- Say **"worm"** to get attention
- Then speak your message
- Say **"quit"** to exit

### **Text Mode**
- Type messages directly
- Type **"quit"** to exit

## 🧩 **Modular Benefits**

### **✅ Separation of Concerns**
- **Core**: Hardware control only
- **AI**: Natural language processing only  
- **Config**: Data management only
- **App**: Orchestration only

### **✅ Easy Testing**
```python
# Test hardware without AI
from core import WormController
worm = WormController()
worm.dance_animation()

# Test AI without hardware
from ai import AIProcessor
ai = AIProcessor()
response = ai.generate_response("Hello!")
```

### **✅ Easy Swapping**
- Replace OpenAI with different AI provider
- Replace Arduino with different hardware
- Use different TTS engines
- Swap response management systems

### **✅ Independent Development**
- Work on AI features without hardware
- Develop hardware features without AI
- Test each component separately

## 📁 **File Structure**
```
worm/
├── 📁 core/                    # Hardware & Audio (no AI)
│   ├── worm_controller.py      # Arduino communication
│   ├── audio_controller.py     # Speech & voice recognition
│   └── __init__.py
│
├── 📁 ai/                      # AI Processing (no hardware)
│   ├── ai_processor.py         # OpenAI integration
│   └── __init__.py
│
├── config_manager.py           # Response & settings management
├── worm_system_refactored.py   # Main orchestrator
│
├── 📄 worm_responses.json      # Predefined responses
├── 📄 worm_settings.json       # System settings
├── 📄 openai_key.txt          # API key (gitignored)
│
└── 📄 README.md               # This file
```

## 🔧 **Configuration**

### **Responses**
Edit `worm_responses.json` or use the response editor:
```python
from config_manager import ConfigManager
config = ConfigManager()
config.add_response("greetings", "casual", "Hey there!", "dance_animation")
```

### **Settings**
Modify `worm_settings.json` or programmatically:
```python
config.set_setting("audio.volume", 0.9)
config.set_setting("ai.use_ai_fallback", True)
```

## 🤖 **Hardware Commands**

Available Arduino commands:
- `dance_animation()` - Dance sequence
- `talk_animation()` - Talking mouth movement
- `choreographed_talk()` - Complex talking animation
- `sadness_movement()` - Sad emotion display
- `move_forward_left()` - Movement controls
- `open_mouth()` / `close_mouth()` - Manual mouth control
- `reset_position()` - Return to neutral

## 🧠 **AI Features**

- **Intent Analysis**: Understands user intent (question, command, conversation)
- **Emotion Detection**: Detects emotional context
- **Movement Suggestions**: AI suggests appropriate movements
- **Conversation Memory**: Remembers recent conversation context
- **Fallback Handling**: Graceful handling when AI is unavailable

## 📊 **System Status**

Check system health:
```python
from worm_system_refactored import WormSystem
worm = WormSystem()
stats = worm.get_system_stats()
print(stats)
```

## 🔒 **Security**

- API keys are gitignored
- No secrets in source code
- Environment variable support
- Secure credential handling

## 🛠️ **Development**

### **Adding New Hardware Features**
Edit `core/worm_controller.py` - no AI changes needed

### **Adding New AI Capabilities**  
Edit `ai/ai_processor.py` - no hardware changes needed

### **Adding New Responses**
Edit `config_manager.py` or use the JSON file directly

### **Extending the Orchestrator**
Edit `worm_system_refactored.py` to coordinate new features

## 🐛 **Troubleshooting**

### **Hardware Issues**
- Check serial port connection
- Verify Arduino sketch is loaded
- System runs in simulation mode if hardware unavailable

### **AI Issues**  
- Verify OpenAI API key is valid
- Check internet connection
- System falls back to predefined responses

### **Audio Issues**
- Check microphone permissions
- Verify pygame audio setup
- Install audio dependencies

## 📈 **Migration from Old System**

The old `worm_system.py` mixed all concerns. The new architecture provides:

- **Better testability**
- **Easier maintenance**  
- **Cleaner code separation**
- **Independent feature development**
- **Easy component swapping**

Run both systems side-by-side during transition.

---
**🐛 Happy worming!** 🤖 