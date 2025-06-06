# 📝 Worm Response Syntax Guide

## 🔍 Quick Category Reference

### 🎤 GREETINGS (What worm SAYS automatically)
```
"startup" → Spoken when worm starts up
"hello_there_worm" → Spoken when you say "hello there worm"  
"nice_to_meet_you" → Spoken when you say "nice to meet you"
```

### 🤖 COMMAND RESPONSES (What worm SAYS when moving)
```
"fl" → Forward/left tilt    (triggered by "move forward", "go ahead")
"fr" → Forward/right tilt   (triggered by "turn right", "go right") 
"bl" → Back/left tilt       (triggered by "lean back left")
"br" → Back/right tilt      (triggered by "lean back right")
"b"  → Reset to center      (triggered by "reset", "center")
"t"  → Talk sequence        (triggered by "talk", "chat")
"d"  → Dance sequence       (triggered by "dance", "party")
"om" → Open mouth          (triggered by "open mouth") [SILENT]
"cm" → Close mouth         (triggered by "close mouth") [SILENT]
```

### ✨ CUSTOM CATEGORIES (Future: Each has its own movement!)
```
"encouragement" → Gentle forward-backward rocking with supportive gestures
"excitement" → Quick energetic side-to-side wiggles 
"curiosity" → Slow inquisitive head tilts and gentle swaying
"relaxation" → Slow, flowing wave-like motion
"celebration" → Enthusiastic full-body celebration movements
"compliments" → Gentle, humble swaying with shy mouth movements  
"jokes" → Playful bouncing motion with chuckling
"short_responses" → Quick, simple acknowledgment gesture
```

## 💬 Input → Output Flow

### Normal Commands:
```
User says: "move forward"
→ AI translates to: "fl" 
→ Worm does: forward tilt movement
→ Worm says: your "fl" response
```

### Special Commands:
```
User says: "hello there worm"
→ Worm does: choreographed mouth movement
→ Worm says: your "hello_there_worm" response
```

### Custom Categories (Future Implementation):
```
User says: "cheer me up"
→ AI detects: encouragement intent
→ Worm does: encouragement movement + talk sequence
→ Worm says: random response from "encouragement" category
```

## 🎯 Smart Mouth Movement

**Short responses (≤5 words):**
- Example: "Hello there!" (2 words)
- Gets: **1 mouth movement**

**Long responses (>5 words):**
- Example: "Hello there, thanks for turning me back on!" (8 words)  
- Gets: **2 mouth movements** (spaced during speech)

## ✅ Adding Custom Responses - New Clear Interface!

### Step-by-Step:
1. Run: `python3 edit_worm_responses.py`
2. Choose **5** (Add to existing category)
3. **Select category** from numbered list (1-8)
4. **Enter Speech Output:** What the worm will SAY
5. **Preview** shows word count and mouth movements
6. **Confirm** to save

### Example Session:
```
Select category: 2 (encouragement)
Enter Speech Output: You're doing amazing, keep it up!
Preview: 7 words = 2 mouth movements
Save? y
✅ Added to encouragement!
```

## 🛠️ Editor Features

- **Clear category explanations** - Know exactly what each does
- **Input vs Output clarity** - No confusion about what gets spoken
- **Word count preview** - See mouth movements before saving
- **Syntax validation** - Prevents common quote errors
- **Category management** - Add to existing or create new categories

## 🎬 Hardware-Optimized Movements

Each movement uses the servo-tendon system effectively:
- **FL/FR/BL/BR servos** create peristaltic (wave-like) body motion
- **MID servo** controls mouth sync with speech
- **Movements embody emotional tone** of each category
- **Medium-sized sequences** that flow naturally with speech

## ✅ Correct Syntax Examples

```json
"startup": "Hello there, I'm your worm friend!"
"fl": "Moving forward with excitement!"
"d": "Let's dance!"
```

## ❌ Common Syntax Errors

```json
❌ "startup": Hello there     (missing quotes)
❌ "fl": "Let's "dance""      (nested quotes)
❌ "d": "Let's dance!,        (missing closing quote)
```

## 🛠️ Using the Editor

1. Run: `python3 edit_worm_responses.py`
2. Choose option 6 for detailed help
3. Each edit shows:
   - What triggers the response
   - Current word count & mouth movements
   - Preview before saving 