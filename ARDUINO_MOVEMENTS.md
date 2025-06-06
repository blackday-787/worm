&*'kj
L# 🤖 ARDUINO MOVEMENT COMMANDS

## Current Movement Commands

| Command | Function | Description |
|---------|----------|-------------|
| `fl` | Forward Left | Tilt front left (moving forward) |
| `fr` | Forward Right | Tilt front right (turning right) |
| `bl` | Back Left | Tilt back left |
| `br` | Back Right | Tilt back right |
| `b` | Base/Neutral | Reset to neutral position |
| `om` | Open Mouth | Open mouth servo |
| `cm` | Close Mouth | Close mouth servo |
| `t` | Talk | Choreographed talking sequence |
| `d` | Dance | Dance sequence |
| `choreographedTalk` | Special Talk | Custom choreographed talk movement |

## NEW MOVEMENT TO IMPLEMENT

### `sadness` - Sad Forward Lean
**Purpose**: Lean the worm forward slowly as if it is sad
**Description**: A slow, gentle forward lean that conveys sadness/disappointment
**Usage**: For emotional responses like "im so sorry that the mariners lost dad"

**MOVEMENT SPECIFICATION**:
- **Pull front two motors (fr and fl) MUCH farther forward** than normal movements
- Creates a pronounced forward lean/droop
- Should be slower than normal movements to convey sadness
- Hold the position during speech, then return to neutral

**IMPORTANT - OVERLAY BEHAVIOR**: 
The `sadness` movement will run simultaneously with mouth movements (`t` commands). When the Python system sends:
1. `sadness` (main movement starts)
2. `t` (mouth movement overlays immediately during speech)
3. `t` (additional mouth movements during speech if configured)

The Arduino should handle both movements running together, not sequentially.

**Suggested Implementation**:
```cpp
void sadnessMovement() {
  // Pull front two motors (fr and fl) MUCH farther forward
  // More extreme forward position than normal fl/fr movements
  // Slow, deliberate movement to convey sadness
  // Create a pronounced forward droop/lean
  // Hold the position during speech
  // MUST work with simultaneous mouth movements (t commands)
  
  // Example pseudo-code:
  // frontLeftServo.write(EXTREME_FORWARD_POSITION);   // Much farther than normal
  // frontRightServo.write(EXTREME_FORWARD_POSITION);  // Much farther than normal
  // delay for slow, sad movement
}
```

**Arduino Code Addition Needed**:
Add this case to your main command parser:
```cpp
case 's':
  if (command == "sadness") {
    sadnessMovement();
    Serial.println("Sadness movement complete");
  }
  break;
```

## Movement Overlay System

**NEW BEHAVIOR**: Mouth movements (`t`) now overlay and merge with main movements instead of being sequential.

**Sequence for responses with speech**:
1. Main movement command sent (e.g., `sadness`, `d`, `fl`, etc.)
2. Mouth movements (`t`) sent immediately during speech (overlaid)
3. Both movements run simultaneously
4. Return to neutral (`b`) after both complete

**Benefits**:
- More natural emotional expression
- Mouth moves while body expresses emotion
- No awkward pauses between movement and speech

## Global System Updates Complete

The Python system has been updated to:
- ✅ Include "sadness" in all movement lists in the editor
- ✅ Handle "sadness" movement in the worm system
- ✅ Add fuzzy matching for "dad", "father", "mariners" keywords
- ✅ Add the dad/mariners response with sadness movement
- ✅ Make sadness movement available for other custom responses
- ✅ **NEW**: Overlay mouth movements with main movements
- ✅ **NEW**: All responses now use overlay behavior for natural expression

**Next Step**: Implement the `sadnessMovement()` function on the Arduino side with overlay support. 