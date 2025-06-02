# 🤖 WORM Robot - Modular Architecture

A conversational AI robot with separated AI and hardware layers for independent development and testing.

## 🏗️ Architecture Overview

### Core Components
- `core/` - Pure hardware control (no AI dependencies)
- `ai/` - Pure AI processing (no hardware dependencies)  
- `config_manager.py` - Response JSON and settings management
- `worm_system_refactored.py` - Main orchestrator

### Legacy Backup
- `legacy/` - All original files safely preserved

## 🚀 Quick Start

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. 🤖 Arduino Setup

**Upload the Arduino Sketch:**
```bash
# Check Arduino connection
ls /dev/cu.*

# Upload the proper sketch
arduino-cli upload -p /dev/cu.usbmodem1401 --fqbn arduino:avr:uno worm_controller.ino
```

**Hardware Requirements:**
- Arduino Uno/Mega
- PCA9685 servo driver board  
- 5 servos (FL, FR, BL, BR, MID for mouth)
- Proper wiring as per servo channels

**Arduino Libraries Needed:**
```cpp
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
```

### 3. Set Environment Variables
```bash
export OPENAI_API_KEY="your_key_here"
export WORM_SERIAL_PORT="/dev/cu.usbmodem1401"  # Update as needed
```

### 4. Run the System
```bash
# Full orchestrated system
python3 worm_system_refactored.py

# Test individual components
python3 demo_modular_architecture.py
```

## 🔧 Arduino Communication

**Python → Arduino Communication:**
- Python sends simple string commands via serial
- Arduino listens on `Serial.readStringUntil('\n')`
- Baud rate: 115200

**Available Commands:**
- `fl` - Tilt front left
- `fr` - Tilt front right  
- `bl` - Tilt back left
- `br` - Tilt back right
- `b` - Reset to neutral
- `t` - Choreographed talk animation
- `d` - Dance animation
- `om` - Open mouth
- `cm` - Close mouth
- `sadness` - Sadness movement
- `ta` - Test all movements

**Arduino Response:**
- Confirms each command received
- Provides status updates
- Reports completion of animations

## 🧪 Testing Components

### Hardware Only (No AI)
```python
from core.worm_controller import WormController

worm = WormController()
worm.dance_animation()    # Test without AI
worm.talk_animation()     # Works independently
```

### AI Only (No Hardware)  
```python
from ai.ai_processor import AIProcessor

ai = AIProcessor()
response = ai.process("Tell me a joke")  # No hardware needed
print(response)
```

### Audio Only
```python
from core.audio_controller import AudioController

audio = AudioController()
audio.speak("Hello world")      # TTS test
text = audio.listen()           # Speech recognition test
```

## 🔍 Troubleshooting

### Arduino Connection Issues
```bash
# Check available ports
ls /dev/cu.*

# Test serial connection
screen /dev/cu.usbmodem1401 115200

# In the Arduino Serial Monitor, type: ta
# Should see: "🧪 Testing all movements..."
```

### Python Serial Issues
```python
# Test basic serial communication
python3 -c "
from core.worm_controller import WormController
worm = WormController()
worm.send_command('ta')  # Should trigger test sequence
"
```

### Missing Libraries
```bash
# Arduino libraries
# Install through Arduino IDE Library Manager:
# - Adafruit PWM Servo Driver Library
# - Wire (built-in)

# Python libraries
pip install -r requirements.txt
```

## 📝 Development

### Adding New Movements
1. **Arduino side:** Add function in `worm_controller.ino`
2. **Python side:** Add method in `core/worm_controller.py`
3. **AI side:** Update prompts in `ai/ai_processor.py`

### Adding New AI Features
- Modify `ai/ai_processor.py` only
- Hardware layer remains untouched
- Test AI features without physical robot

### Hardware Development
- Modify `core/` components only  
- AI layer remains untouched
- Test hardware without AI processing

## 🔄 System Flow

```
User Input → AI Processor → Movement Commands → Arduino → Physical Movement
                ↓                    ↓              ↓
            Generates Intent    Translates to     Controls
            & Response          Serial Commands   Servos
```

## 📊 Project Stats

- **Modular Components:** 6 independent packages
- **Legacy Files Preserved:** 36 files in organized backup
- **Zero Dependencies** between AI and hardware layers
- **Independent Testing** for each component

## 🎯 Next Steps

1. **Test your Arduino connection**
2. **Upload `worm_controller.ino`**  
3. **Run the demo script**
4. **Start developing new features!**

---

*Happy modular worming! 🐛🤖* 