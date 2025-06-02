#!/bin/bash

# 🧹 WORM PROJECT CLEANUP SCRIPT
# Safely moves legacy files to backup directory
# Run after refactoring to clean up the project

echo "🧹 WORM PROJECT CLEANUP"
echo "======================"
echo "This script will move legacy files to 'legacy/' directory"
echo "Your new refactored system will remain untouched!"
echo ""

# Create backup directories
echo "📁 Creating backup directories..."
mkdir -p legacy/old_system
mkdir -p legacy/unrelated_features
mkdir -p legacy/reference_files
mkdir -p legacy/duplicates

# Function to safely move files
safe_move() {
    local file="$1"
    local destination="$2"
    if [ -f "$file" ]; then
        echo "  📦 Moving: $file → $destination/"
        mv "$file" "$destination/"
    elif [ -d "$file" ]; then
        echo "  📦 Moving directory: $file → $destination/"
        mv "$file" "$destination/"
    else
        echo "  ⚠️  Not found: $file"
    fi
}

echo ""
echo "🔄 Moving legacy system files..."
echo "These were replaced by the modular refactor:"

# Legacy system components (replaced by refactor)
safe_move "main.py" "legacy/old_system"
safe_move "get_text_input.py" "legacy/old_system"
safe_move "speech_input_mode.py" "legacy/old_system"
safe_move "gpt_interpreter.py" "legacy/old_system"
safe_move "input_manager.py" "legacy/old_system"
safe_move "interpreter.py" "legacy/old_system"
safe_move "output_handler.py" "legacy/old_system"

# Legacy hardware control
safe_move "control_steppers.py" "legacy/old_system"
safe_move "steppers_control.py" "legacy/old_system"
safe_move "test_serial.py" "legacy/old_system"

echo ""
echo "🔄 Moving unrelated features..."
echo "These aren't part of the robot system:"

# Unrelated features
safe_move "app.py" "legacy/unrelated_features"
safe_move "fetch_google_doc.py" "legacy/unrelated_features"
safe_move "client_secrets.json" "legacy/unrelated_features"
safe_move "ide.py" "legacy/unrelated_features"

echo ""
echo "🔄 Moving reference/documentation files..."
echo "These might be useful for reference:"

# Reference files
safe_move "prompt_context.txt" "legacy/reference_files"
safe_move "prd_may17.txt" "legacy/reference_files"
safe_move "commit_all.sh" "legacy/reference_files"

echo ""
echo "🔄 Moving duplicate directories..."
echo "These contain duplicates of files already moved:"

# Duplicate directories
safe_move "reference txt" "legacy/duplicates"

# Clean up cache and system files
echo ""
echo "🗑️  Removing auto-generated files..."
if [ -d "__pycache__" ]; then
    echo "  🗑️  Removing __pycache__/"
    rm -rf __pycache__
fi

if [ -f ".DS_Store" ]; then
    echo "  🗑️  Removing .DS_Store"
    rm -f .DS_Store
fi

# Empty tests directory
if [ -d "tests" ] && [ -z "$(ls -A tests)" ]; then
    echo "  🗑️  Removing empty tests/ directory"
    rmdir tests
fi

echo ""
echo "📊 CLEANUP SUMMARY"
echo "=================="
echo ""

# Show what's left in the main directory
echo "✅ YOUR CLEAN PROJECT NOW CONTAINS:"
echo ""
echo "🏗️  NEW MODULAR ARCHITECTURE:"
ls -la core/ ai/ 2>/dev/null | head -3
echo "   core/ - Hardware & audio control (no AI)"
echo "   ai/ - AI processing (no hardware)"
echo ""

echo "🎯 MAIN SYSTEM FILES:"
echo "   config_manager.py - Configuration management"
echo "   worm_system_refactored.py - Main orchestrator"
echo "   demo_modular_architecture.py - Component demos"
echo "   README.md - Complete documentation"
echo ""

echo "🤖 ESSENTIAL ARDUINO FILES:"
[ -f "worm_1.0.ino" ] && echo "   ✅ worm_1.0.ino"
[ -f "arduino_ino_5-26.txt" ] && echo "   ✅ arduino_ino_5-26.txt"
[ -f "requirements.txt" ] && echo "   ✅ requirements.txt"
echo ""

echo "📦 BACKUP FILES PRESERVED IN:"
echo "   legacy/old_system/ - Original worm system files"
echo "   legacy/unrelated_features/ - Flask app, Google Docs, etc."
echo "   legacy/reference_files/ - Documentation and prompts"
echo "   legacy/duplicates/ - Duplicate directories"
echo ""

# Count files moved
legacy_count=$(find legacy -type f 2>/dev/null | wc -l | tr -d ' ')
echo "📈 STATS:"
echo "   🗂️  Files moved to legacy/: $legacy_count"
echo "   🧹 Cache files removed"
echo "   ✨ Project is now clean and focused!"
echo ""

echo "🎉 CLEANUP COMPLETE!"
echo ""
echo "🚀 TO RUN YOUR NEW SYSTEM:"
echo "   python3 worm_system_refactored.py"
echo ""
echo "🎯 TO SEE COMPONENT DEMOS:"
echo "   python3 demo_modular_architecture.py"
echo ""
echo "📚 FOR DOCUMENTATION:"
echo "   cat README.md"
echo ""
echo "🔄 TO RESTORE FILES (if needed):"
echo "   mv legacy/old_system/* .  # Restore old system"
echo ""
echo "🐛 Happy modular worming! 🤖" 