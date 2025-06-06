#!/usr/bin/env python3
"""
🎯 WORM MODULAR ARCHITECTURE DEMO (AI-FREE)
Demonstrates how to use each component independently and together
Now includes the new Response Editor for managing responses
"""

import time
import sys

def demo_hardware_only():
    """Demo: Pure hardware control without AI"""
    print("\n🤖 DEMO 1: Hardware Control Only")
    print("=" * 50)
    
    try:
        from core import WormController
        
        print("🔧 Initializing hardware controller...")
        worm = WormController()
        
        print("🎭 Testing movements...")
        movements = [
            ("d", "Dancing! 💃"),
            ("t", "Talking animation"),
            ("s", "Showing sadness 😢"),
            ("b", "Resetting to neutral")
        ]
        
        for movement, description in movements:
            print(f"  🎯 {description}")
            worm.send_command(movement)
            time.sleep(1.5)
        
        worm.close()
        print("✅ Hardware demo complete!")
        
    except Exception as e:
        print(f"❌ Hardware demo error: {e}")

def demo_config_only():
    """Demo: Configuration management with predefined responses"""
    print("\n⚙️ DEMO 2: Configuration Management (Predefined Responses)")
    print("=" * 60)
    
    try:
        from config_manager import ConfigManager
        
        print("📁 Initializing configuration manager...")
        config = ConfigManager()
        
        print(f"📊 Loaded {config.get_response_count()} predefined responses")
        
        print("\n🔍 Testing response lookup...")
        test_queries = [
            "hello",
            "dance", 
            "what are you",
            "I'm happy",
            "random query that won't match"
        ]
        
        for query in test_queries:
            print(f"\n🔎 Query: '{query}'")
            response = config.find_response(query)
            if response:
                print(f"📖 Response: {response.text}")
                if response.movement:
                    print(f"🎭 Movement: {response.movement}")
            else:
                print("❌ No matching response found")
        
        # Demo adding a new response
        print("\n➕ Adding a new response...")
        config.add_response(
            "demo", 
            "test", 
            "This is a demo response!", 
            "dance_animation"
        )
        
        # Demo settings
        print("\n⚙️ Settings demo...")
        config.set_setting("demo.test_setting", "Hello World")
        value = config.get_setting("demo.test_setting")
        print(f"📝 Setting value: {value}")
        
        # Show stats
        stats = config.get_stats()
        print(f"\n📊 Config stats: {stats}")
        
        print("✅ Configuration demo complete!")
        
    except Exception as e:
        print(f"❌ Configuration demo error: {e}")

def demo_audio_only():
    """Demo: Audio functionality with TTS"""
    print("\n🎤 DEMO 3: Audio Control (Text-to-Speech)")
    print("=" * 50)
    
    try:
        from core import AudioController
        
        print("🔊 Initializing audio controller...")
        audio = AudioController()
        
        print("🗣️ Testing text-to-speech...")
        test_phrases = [
            "Hello! I'm testing the text-to-speech system.",
            "This is the AI-free WORM architecture.",
            "Text-to-speech works perfectly without AI!",
            "I can speak any text you give me!"
        ]
        
        for phrase in test_phrases:
            print(f"🗣️ Speaking: '{phrase}'")
            audio.speak(phrase, blocking=True)
            time.sleep(0.5)
        
        print("🎤 Testing voice recognition setup...")
        if audio.setup_voice_recognition():
            print("✅ Voice recognition is available")
        else:
            print("⚠️  Voice recognition not available (need Vosk model)")
        
        audio.close()
        print("✅ Audio demo complete!")
        
    except Exception as e:
        print(f"❌ Audio demo error: {e}")

def demo_response_editor():
    """Demo: Response Editor functionality"""
    print("\n📝 DEMO 4: Response Editor")
    print("=" * 30)
    
    try:
        print("🚀 The Response Editor allows you to:")
        print("  📖 Browse existing responses")
        print("  ➕ Add new responses")
        print("  🎤 Test text-to-speech")
        print("  👀 Preview responses with TTS")
        print("  📥📤 Import/export responses")
        print("  📊 View statistics")
        
        print("\n💡 To launch the Response Editor:")
        print("   python response_editor.py")
        
        print("\n🎯 Quick test - loading config...")
        from config_manager import ConfigManager
        config = ConfigManager()
        print(f"✅ {config.get_response_count()} responses available for editing")
        
        print("✅ Response Editor demo complete!")
        
    except Exception as e:
        print(f"❌ Response Editor demo error: {e}")

def demo_full_integration():
    """Demo: Full system integration (AI-free)"""
    print("\n🌟 DEMO 5: Full System Integration (AI-Free)")
    print("=" * 55)
    
    try:
        from worm_system_refactored import WormSystem
        
        print("🚀 Initializing AI-free WORM system...")
        worm = WormSystem()
        
        # Show system status
        stats = worm.get_system_stats()
        print("\n📊 System Status:")
        print(f"  🤖 Hardware: {'✅ Connected' if stats['hardware']['connected'] else '🤖 Simulation'}")
        print(f"  🎤 Audio/TTS: {'✅ Ready' if stats['audio']['tts_functional'] else '❌ Error'}")
        print(f"  🧠 AI: {stats['ai']['status']} ({'✅' if stats['ai']['available'] else '❌'})")
        print(f"  ⚙️  Responses: {stats['config']['total_responses']} loaded")
        print(f"  🏃 Mode: {stats['system']['mode']}")
        
        print("\n💬 Testing integrated responses (predefined only)...")
        test_inputs = [
            "hello worm",
            "dance for me",
            "what are you",
            "I'm feeling happy",
            "something completely random"
        ]
        
        print("\n🎯 Processing test inputs:")
        for user_input in test_inputs:
            print(f"\n👤 Input: '{user_input}'")
            result = worm._process_input(user_input)
            print(f"📊 Result: {result['type']} response")
            time.sleep(1)
        
        worm.stop()
        print("\n✅ Full integration demo complete!")
        
    except Exception as e:
        print(f"❌ Full integration demo error: {e}")

def demo_tts_focused():
    """Demo: Focused TTS testing with predefined responses"""
    print("\n🎤 DEMO 6: Text-to-Speech Focus Test")
    print("=" * 45)
    
    try:
        from config_manager import ConfigManager
        from core.audio_controller import AudioController
        
        print("🔊 Initializing TTS components...")
        config = ConfigManager()
        audio = AudioController()
        
        print("🗣️ Testing TTS with various response types...")
        
        # Test different categories
        test_categories = [
            ("hello", "greetings"),
            ("dance", "commands"),
            ("what are you", "questions"),
            ("I'm happy", "emotions")
        ]
        
        for query, expected_category in test_categories:
            print(f"\n🔎 Query: '{query}' (expecting {expected_category})")
            response = config.find_response(query)
            
            if response:
                print(f"📖 Found: {response.text}")
                print(f"🎭 Movement: {response.movement or 'none'}")
                print("🗣️ Playing with TTS...")
                audio.speak(response.text, blocking=True)
                print("✅ TTS complete!")
            else:
                print("❌ No response found")
            
            time.sleep(0.5)
        
        audio.close()
        print("\n✅ TTS focus test complete!")
        
    except Exception as e:
        print(f"❌ TTS focus test error: {e}")

def main():
    """Main demo runner"""
    print("🎯 WORM MODULAR ARCHITECTURE DEMOS (AI-FREE)")
    print("=" * 60)
    print("🎤 Text-to-Speech and predefined responses are fully functional!")
    print("🚫 AI generation has been removed - use Response Editor to add responses")
    print()
    
    demos = [
        ("1", "Hardware Control Only", demo_hardware_only),
        ("2", "Configuration & Predefined Responses", demo_config_only),
        ("3", "Audio Control & TTS", demo_audio_only),
        ("4", "Response Editor", demo_response_editor),
        ("5", "Full System Integration", demo_full_integration),
        ("6", "TTS Focus Test", demo_tts_focused),
        ("A", "Run All Demos", None),
        ("Q", "Quit", None)
    ]
    
    while True:
        print("\n📋 AVAILABLE DEMOS:")
        for code, name, _ in demos:
            icon = "🚀" if code == "A" else "🚪" if code == "Q" else "🎯"
            print(f"  {code}. {icon} {name}")
        
        choice = input("\nSelect demo (1-6, A, Q): ").strip().upper()
        
        if choice == 'Q':
            print("👋 Goodbye!")
            break
        elif choice == 'A':
            print("\n🚀 RUNNING ALL DEMOS...")
            for code, name, demo_func in demos:
                if demo_func:  # Skip A and Q entries
                    print(f"\n{'='*60}")
                    print(f"🎯 RUNNING: {name}")
                    print(f"{'='*60}")
                    demo_func()
                    input("\nPress Enter to continue to next demo...")
            print("\n🎉 All demos completed!")
        else:
            # Find and run specific demo
            demo_found = False
            for code, name, demo_func in demos:
                if code == choice and demo_func:
                    print(f"\n🎯 RUNNING: {name}")
                    demo_func()
                    demo_found = True
                    break
            
            if not demo_found:
                print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 