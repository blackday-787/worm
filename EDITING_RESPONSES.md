# 🐛 Editing Worm Responses - Quick Guide

## The Super Easy Way (Recommended)

**To change the greeting (or any response):**
```bash
python3 edit_worm_responses.py
```

**NEW: Much clearer interface!**
- Shows exactly what triggers each response
- Displays word count and mouth movements
- Explains syntax and gives examples
- Preview before saving
- Choose option 6 for detailed help

This gives you a simple menu to edit:
- Startup greeting ("hello there. thanks for turning me back on")
- Command responses ("I'm wiggling forward with excitement!")
- Special greetings ("Hello there Tate!")
- Error messages

## The Direct File Edit Way

**Step 1:** Open `worm_responses.json` in any text editor

**Step 2:** Find what you want to change:
```json
{
  "greetings": {
    "startup": "'Sup bitches!",           ← Change this line
    "hello_there_worm": "Hello there Tate!",
    "nice_to_meet_you": "Nice to meet you too!"
  },
  "command_responses": {
    "fl": "I'm wiggling forward with excitement!",  ← Or these
    "fr": "Time to turn right and explore!",
    ...
  }
}
```

**Step 3:** Save the file

**Step 4:** Restart the worm system

## What's Where

- **`startup`** - What the worm says when it first starts up
- **`hello_there_worm`** - Response to "hello there worm"
- **`nice_to_meet_you`** - Response to "nice to meet you"
- **`command_responses`** - What the worm says for each movement command
- **`mode_switches`** - Voice/text mode change messages
- **`error_messages`** - What to say when things go wrong

## Examples

**Change greeting to be friendlier:**
```json
"startup": "Hello there! I'm your friendly worm robot!"
```

**Make forward movement more exciting:**
```json
"fl": "WOOHOO! Here I come wiggling forward like a champion!"
```

**Personalize the hello:**
```json
"hello_there_worm": "Well hello there, my awesome human friend!"
```

## Tips

1. **Keep it fun!** The worm has personality
2. **Smart mouth movement** - Short responses (≤5 words) get 1 mouth movement, full sentences get 2 movements
3. **Test changes immediately** - just restart the worm system
4. **Backup first** if you want to experiment wildly

That's it! No coding required - just edit text and restart! 🎉 