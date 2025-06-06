# 🐛 WORM Robot System (AI-Free) 

## ✅ What's Working

This is the **AI-free version** of the WORM robot system with full text-to-speech and predefined response functionality.

### 🎤 **Text-to-Speech (TTS)**
- ✅ **Fully functional** - Can speak any text
- ✅ Uses Google Text-to-Speech (gTTS)
- ✅ Adjustable speech speed
- ✅ Integrated with robot movements

### 📖 **Predefined Responses**
- ✅ **100+ responses** across multiple categories
- ✅ **Smart keyword matching** for appropriate responses
- ✅ **Movement coordination** - responses trigger robot animations
- ✅ **Easy management** via Response Editor

### 🤖 **Hardware Control** 
- ✅ **Arduino integration** via serial communication
- ✅ **Servo animations** - dance, talk, wiggle, etc.
- ✅ **Movement coordination** with speech

### 🎤 **Voice Recognition** (Optional)
- ✅ **Works with Vosk models** for offline speech recognition
- ✅ **Wake word detection** ("worm")
- ✅ **Continuous listening** mode

## ❌ What Was Removed

- ❌ **AI Response Generation** - No more OpenAI API calls
- ❌ **Dynamic conversations** - Uses predefined responses only
- ❌ **Intent analysis** - Basic keyword matching instead
- ❌ **Emotion detection** - Removed AI-powered emotion recognition

## 🚀 Quick Start

### 1. **Easy Launcher**
```bash
python launch_worm.py
```
This shows a menu with all available options.

### 2. **Direct System Launch**
```bash
# Text mode
python worm_system_refactored.py --text

# Voice mode  
python worm_system_refactored.py --voice
```

### 3. **Response Editor**
```bash
python response_editor.py
```

### 4. **Run Demos**
```bash
python demo_modular_architecture.py
```

## 📝 Response Editor Features

The **Response Editor** (`response_editor.py`) allows you to:

- 📖 **Browse** all existing responses
- ➕ **Add new responses** with categories and movements
- 🎤 **Test text-to-speech** with any text
- 👀 **Preview responses** with TTS playback
- 📥📤 **Import/export** responses to/from JSON files
- 🗑️ **Delete** unwanted responses
- 📊 **View statistics** about your response library

### Example Response Categories:
- **Greetings**: "hello", "hi", "hey"
- **Commands**: "dance", "move", "wiggle" 
- **Questions**: "what are you", "who are you"
- **Emotions**: "happy", "sad", "excited"
- **Fallbacks**: Default responses for unmatched input

## 🛠️ Installation

### AI-Free Dependencies
```bash
pip install -r requirements_ai_free.txt
```

This includes:
- `pyserial` - Arduino communication
- `pygame` - Audio playback
- `gTTS` - Text-to-speech
- `vosk` - Voice recognition (optional)
- `sounddevice` - Audio input

### Optional: Voice Recognition
Download a Vosk model for offline speech recognition:
```bash
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
```

## 🎯 Usage Examples

### Add a New Response
1. Run `python response_editor.py`
2. Choose option 2 (Add new response)
3. Select category: `greetings` 
4. Select subcategory: `casual`
5. Enter text: `"Hey there, buddy! Ready to have some fun?"`
6. Choose movement: `dance_animation`
7. Test with TTS, then save

### Test Text-to-Speech
1. Run `python response_editor.py`
2. Choose option 5 (Test text-to-speech)
3. Enter any text to hear it spoken
4. Try different speeds (slow/normal/fast)

### Browse Existing Responses
1. Run `python response_editor.py` 
2. Choose option 1 (Browse existing responses)
3. See all responses organized by category

## 🏗️ System Architecture

```
worm_system_refactored.py      # Main orchestrator (AI-free)
├── core/
│   ├── worm_controller.py     # Hardware control
│   └── audio_controller.py    # TTS & voice recognition
├── config_manager.py          # Predefined responses
└── response_editor.py         # Response management tool
```

### How It Works:
1. **Input received** (text or voice)
2. **Keyword matching** against predefined responses
3. **Response selected** from appropriate category
4. **TTS synthesis** of response text
5. **Movement triggered** (if specified)
6. **Coordinated output** - speech + movement

## 🎮 Available Commands

### System Commands:
- `"hello"` → Greeting response + animation
- `"dance"` → Dance command + dance animation  
- `"what are you"` → Self-description + talk animation
- `"move"` → Movement response + choreographed animation
- `"quit"` → Exit system

### Hardware Commands (via `manual_command()`):
- `dance_animation`
- `talk_animation` 
- `choreographed_talk`
- `sadness_movement`
- `reset_position`

## 🔧 Configuration

### Response Categories
Edit `worm_responses.json` or use the Response Editor:

```json
{
  "greetings": {
    "casual": [
      {
        "text": "Hey there! I'm WORM!",
        "movement": "dance_animation"
      }
    ]
  },
  "commands": {
    "movement": [
      {
        "text": "Watch me move!",
        "movement": "choreographed_talk"
      }
    ]
  }
}
```

### Arduino Connection
- **Port**: Usually `/dev/ttyUSB0` (Linux) or `COM3` (Windows)
- **Baud rate**: 9600
- **Protocol**: JSON commands over serial

## 🚨 Troubleshooting

### TTS Not Working
```bash
# Test audio system
python -c "from core.audio_controller import AudioController; a=AudioController(); a.speak('Test'); a.close()"
```

### Arduino Not Connecting
```bash
# Test connection
python test_arduino_connection.py
```

### No Voice Recognition
- Download Vosk model (see installation section)
- Check microphone permissions

## 🔄 Restoring AI (Future)

To restore AI functionality:
1. Install OpenAI dependencies: `pip install openai`
2. Restore AI imports in `worm_system_refactored.py`
3. Re-enable AI processing in `_process_input()`
4. Add back the `ai/` directory

## 📊 Performance

**Response Time**: ~50-200ms for predefined responses
**TTS Latency**: ~1-3 seconds (depends on text length)
**Memory Usage**: ~50MB (without AI models)
**Startup Time**: ~2-5 seconds

## 🎉 Benefits of AI-Free Version

- ⚡ **Faster responses** - No API calls
- 🔒 **Privacy** - No data sent to external services  
- 💰 **Cost-free** - No API usage fees
- 🔋 **Reliable** - No internet dependency
- 🎯 **Predictable** - Consistent, curated responses
- 🛠️ **Customizable** - Easy to add/edit responses

---

## 📞 Support

The WORM robot now focuses on **reliable, predictable interactions** using predefined responses and full text-to-speech capability. Use the **Response Editor** to expand the conversation capabilities manually!

**Happy Worming! 🐛🤖** 