# WORM Quick Start Guide

## Start WORM System
```bash
python3 start_worm.py
```

**Default: TEXT mode**
- Type messages to WORM
- Type `voice` to switch to voice mode
- Type `quit` to exit

**Voice mode:**
- Say "worm hello" to get attention
- Press `Ctrl+C` to return to text mode

---

## Edit Responses
```bash
python3 edit_responses.py
```

- Create new responses with input/output
- Choose talking animations (1t, 2t, 3t, etc.)
- Select movement commands (d, s, fl, fr, etc.)
- Edit existing responses

---

## Arduino Commands Available:
- **d** - Dance
- **s** - Sadness
- **fl** - Forward Left
- **fr** - Forward Right
- **bl** - Back Left  
- **br** - Back Right
- **sl** - Side Left (channel 5)
- **sr** - Side Right (channel 6)
- **b** - Reset position
- **om** - Open Mouth
- **cm** - Close Mouth

---

## Quick Start:
1. `python3 start_worm.py` - Start main system
2. `python3 edit_responses.py` - Create/edit responses

Simple and clean! 