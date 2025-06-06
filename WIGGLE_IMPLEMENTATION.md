# Wiggle Implementation for Channels 5 & 6

## Overview
This implementation provides proper control for channels 5 (SR - Side Right) and 6 (SL - Side Left) to create a wiggling motion for the WORM robot.

## Hardware Configuration
- **Channel 5 (SR)**: Side Right servo - counteracts by pulling when SL releases
- **Channel 6 (SL)**: Side Left servo - counteracts by pulling when SR releases  
- **Default Position**: Both servos start at 90 degrees (neutral)
- **Pull Position**: 180 degrees (maximum tension)
- **Release Position**: 0 degrees (minimum tension)

## Arduino Commands

### Basic Commands
- `sr` - Single wiggle right (SR pulls, SL releases)
- `sl` - Single wiggle left (SL pulls, SR releases)
- `w` - **NEW: Continuous wiggle motion** (6 cycles of alternating pulls)

### Test Commands  
- `tsr` - Test SR channel only (180° → 0° → 90°)
- `tsl` - Test SL channel only (180° → 0° → 90°)
- `tboth` - Test both channels in opposition
- `diag` - Hardware diagnostic for channels 5 & 6
- `ch5` - Direct test of channel 5
- `ch6` - Direct test of channel 6

### Control Commands
- `b` - Reset all servos to neutral (including channels 5 & 6)

## Python Integration

### WormController Methods
```python
controller.side_left()          # Send "sl" command
controller.side_right()         # Send "sr" command  
controller.wiggle_continuous()  # Send "w" command (NEW)
controller.reset_position()     # Send "b" command
```

### Direct Command Execution
```python
# Any of these commands can be sent directly:
controller.send_command("w")     # Continuous wiggle
controller.send_command("sr")    # Single right wiggle
controller.send_command("sl")    # Single left wiggle
```

## Voice/Text Interaction
Users can trigger wiggle motion with natural language:
- Say "wiggle" → triggers continuous wiggle motion with response
- Direct commands: "w", "sr", "sl" are recognized

## Timing & Delays

### Continuous Wiggle Sequence (`w` command):
1. **Initialize**: Both servos to 90° (neutral)
2. **Phase 1**: SR→180°, delay 50ms, SL→0°, hold 300ms
3. **Phase 2**: SL→180°, delay 50ms, SR→0°, hold 300ms
4. **Repeat**: 6 complete cycles (about 4 seconds total)
5. **Finish**: Both servos return to 90° (neutral)

### Single Wiggles (`sr`/`sl` commands):
- Brief neutral positioning (50ms delay)
- Simultaneous opposing movements (10ms between commands)

## Testing

### Quick Test
```bash
python3 test_wiggle_channels.py
```

### Manual Testing
1. Connect to Arduino
2. Send `w` for full wiggle sequence
3. Send `b` to reset
4. Send `tsr` or `tsl` to test individual channels

## Troubleshooting

### Common Issues
1. **Only one servo moving**: Check wiring on PWM board channels 5 & 6
2. **No movement**: Verify Arduino is receiving commands with `diag`
3. **Erratic movement**: Check servo power supply and connections

### Debug Commands
- `diag` - Tests both channels with progressive angles
- `ch5`/`ch6` - Direct channel testing
- `b` - Reset if servos get stuck in wrong position

## Key Features
✅ **Proper Delays**: 50ms between opposing movements to prevent conflicts  
✅ **Neutral Starting**: Always begins from 90° position  
✅ **Full Opposition**: When one servo pulls (180°), the other releases (0°)  
✅ **Natural Integration**: Works with voice commands and text input  
✅ **Safe Reset**: Always returns to neutral after wiggle sequence 