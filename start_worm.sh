#!/bin/bash

# 🐛 WORM SYSTEM STARTUP SCRIPT
# Automatic startup with Arduino upload and venv handling

echo "🐛 Starting WORM Control System..."
echo "=================================="

# Change to script directory
cd "$(dirname "$0")"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Check if virtual environment exists and activate it
if [ -d "venv" ]; then
    echo "🔄 Activating virtual environment..."
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "📦 Virtual environment will be created automatically..."
fi

# Upload Arduino sketch first
echo ""
echo "🤖 ARDUINO SETUP"
echo "=================="
python3 arduino_uploader.py

# Capture Arduino upload result
arduino_exit_code=$?

if [ $arduino_exit_code -eq 0 ]; then
    echo "✅ Arduino setup complete"
else
    echo "⚠️  Arduino setup failed - continuing in simulation mode"
fi

# Run the comprehensive launcher
echo ""
echo "🚀 LAUNCHING WORM SYSTEM"
echo "========================="
python3 launch_worm.py "$@"

# Capture exit code
exit_code=$?

if [ $exit_code -ne 0 ]; then
    echo ""
    echo "❌ Worm system exited with error code: $exit_code"
    echo "Check the output above for details."
else
    echo ""
    echo "👋 Worm system shutdown complete."
fi

exit $exit_code 