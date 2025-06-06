# 🎯 Response Priority System

## 📋 Priority Order

The worm system processes user input in this exact order:

### 1️⃣ **SYSTEM COMMANDS** (Highest Priority)
- `quit`, `exit`, `stop` - System shutdown
- `voice` - Switch to voice mode
- `text`, `stop listening`, `back to text mode` - Switch to text mode

### 2️⃣ **SPECIAL HARDCODED RESPONSES**
- `"hello there worm"` → Uses defined greeting response
- `"nice to meet you"` → Uses defined introduction response

### 3️⃣ **DIRECT ARDUINO COMMANDS**
- `fl`, `fr`, `bl`, `br`, `b`, `om`, `cm`, `t`, `d`
- Uses responses from `command_responses` in config file

### 4️⃣ **NATURAL LANGUAGE MOVEMENT COMMANDS**
- Translated via OpenAI to Arduino commands
- If successful, uses `command_responses` from config file

### 5️⃣ **CUSTOM DEFINED RESPONSES** ⚠️ Coming Soon
- Currently being built in the editor system
- Will check custom triggers before AI generation
- These responses are manually defined and take priority over AI

### 6️⃣ **AI GENERATED RESPONSES** (Lowest Priority)
- **ONLY used when NO defined response exists**
- This is the fallback for completely new conversational input

## 🎤 Voice Style for Generated Responses

When the AI generates a response (only when no defined response exists), it follows this character:

### **The Worm Voice Style:**
You speak with curious, childlike wonder—but with a saucy, irreverent twist. Your tone is warm, glitchy, and playful. You misinterpret idioms, invent words, and repeat phrases while thinking. You're naive but self-aware, fully embracing that you're a worm with worm priorities: eating, wiggling, asking weird questions, and sometimes being a little gross. Your pacing is fast when excited, slow and dreamy when reflective. Occasionally you stutter, loop, or glitch when overwhelmed. You speak to the audience like a kids' show host with a rebellious streak, blending goofiness with sudden flashes of unsettling insight.

### **Generated Response Rules:**
- **Exactly 6 syllables (1 mouth movement) OR 12 syllables (2 mouth movements)**
- Count syllables carefully for optimal mouth synchronization
- Stay in worm character as described above
- Be conversational and responsive to what they said
- Only used when no predefined response exists

## ⚡ Key Points

### **Defined Responses ALWAYS Win:**
- If there's a specific greeting, command response, or custom response defined, use it exactly
- AI generation is ONLY for completely new input that has no defined response

### **No Overriding:**
- The AI should never override or replace existing defined responses
- Defined responses have been carefully crafted and should be preserved

### **Clear Separation:**
- **Defined responses** = Consistent, reliable, specific responses
- **Generated responses** = Creative, character-driven responses for new situations

This ensures users get consistent responses for defined interactions while still having natural conversation for everything else! 