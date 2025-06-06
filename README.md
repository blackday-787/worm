# 🐛 Worm Robot Control System

A robotic worm control system with Arduino integration, AI-powered natural language processing, and **fully conversational** male voice feedback with synchronized mouth movement.

## Quick Start

**Run the worm system:**
```bash
./start_worm.sh
```

This command will automatically:
- ✅ Set up virtual environment
- ✅ Install all dependencies  
- ✅ Upload Arduino sketch
- ✅ Configure AI features
- ✅ Launch the control system

## ✨ Features

- **🗣️ Fully Conversational**: Every command gets a voice response with mouth movement
- **🤖 AI Natural Language Processing**: Say things like "move forward", "dance", "open mouth"
- **👨 Deep Male Voice**: Responds with a conversational male voice
- **🎭 Realistic Mouth Movement**: 't' command triggers complex mouth animations during speech
- **🎤 Voice Control**: Switch between text and voice input modes
- **📱 Arduino Integration**: Real-time servo control
- **🔄 Automatic Setup**: One command does everything

## Usage

### Conversational Experience
**The worm talks back to EVERYTHING you say!** 

Type or say:
- `"move forward"` → Worm says "Moving forward" + moves + mouth animates
- `"dance"` → Worm says "Let's dance" + dances + mouth animates
- `"open mouth"` → Worm says "Opening mouth" + opens mouth + mouth animates
- `"fl"` → Worm says "Moving front left" + moves + mouth animates

### Special Commands
- `"hello there worm"` → Worm says "Hello there Tate!" with special choreographed mouth movement
- `"nice to meet you"` → Worm says "Nice to meet you too!" and does a little dance

### System Commands
- `voice` - Switch to voice input mode (worm says "Voice mode activated")
- `text` - Switch to text input mode (worm says "Text mode activated")
- `help` - Show all commands
- `quit` - Exit system (worm says "Goodbye!")

### Mode Switching
- **📱 In TEXT mode**: Type `voice` to switch to voice input
- **🎤 In VOICE mode**: Say `text` to switch back to text input

### Direct Arduino Commands (still work)
- `fl`, `fr`, `bl`, `br` - Directional tilts
- `b` - Reset to neutral position
- `om`, `cm` - Open/close mouth
- `t` - Talk sequence (complex mouth movement)
- `d` - Dance routine

## Hardware Requirements

- Arduino Uno/Nano (or compatible)
- Adafruit PCA9685 PWM Servo Driver
- 5x Servo Motors (standard size)
- USB cable for Arduino connection

### Servo Connections
```
PCA9685 Channel → Function
0 → Front Left (FL)
1 → Front Right (FR)
2 → Back Left (BL)  
3 → Front Right (BR)
4 → Mouth (MO)
```

## AI Features

✅ **Already Configured!** Your OpenAI API key is set up and working.

The system uses GPT-4 to understand natural language and translate it to worm commands. Voice responses use a male voice for feedback. 