#!/bin/bash

echo "Setting up Arduino CLI for auto-upload functionality..."

# Check if arduino-cli is already installed
if command -v arduino-cli &> /dev/null; then
    echo "Arduino CLI already installed"
    arduino-cli version
else
    echo "Installing Arduino CLI..."
    
    # Install using Homebrew on macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        if command -v brew &> /dev/null; then
            brew install arduino-cli
        else
            echo "Please install Homebrew first: https://brew.sh/"
            exit 1
        fi
    else
        echo "Please install Arduino CLI manually: https://arduino.github.io/arduino-cli/"
        exit 1
    fi
fi

# Configure Arduino CLI
echo "Configuring Arduino CLI..."
arduino-cli config init
arduino-cli core update-index
arduino-cli core install arduino:avr

echo "Installing required libraries..."
arduino-cli lib install "Adafruit PWM Servo Driver Library"

echo "Arduino CLI setup complete!"
echo "Auto-upload will now work when you run the WORM system." 