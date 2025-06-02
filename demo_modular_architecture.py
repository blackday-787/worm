#!/usr/bin/env python3
"""
🎯 WORM MODULAR ARCHITECTURE DEMO
Demonstrates how to use each component independently and together
"""

import time
import sys

def demo_hardware_only():
    """Demo: Pure hardware control without AI"""
    print("\n🤖 DEMO 1: Hardware Control Only (No AI)")
    print("=" * 50)
    
    try:
        from core import WormController
        
        print("🔧 Initializing hardware controller...")
        worm = WormController()
        
        print("🎭 Testing movements...")
        movements = [
            ("dance_animation", "Dancing! 💃"),
            ("talk_animation", "Talking animation"),
            ("choreographed_talk", "Choreographed talking"),
            ("sadness_movement", "Showing sadness 😢"),
            ("reset_position", "Resetting to neutral")
        ]
        
        for movement, description in movements:
            print(f"  🎯 {description}")
            getattr(worm, movement)()
            time.sleep(1.5)
        
        worm.close()
        print("✅ Hardware demo complete!")
        
    except Exception as e:
        print(f"❌ Hardware demo error: {e}")

def demo_ai_only():
    """Demo: Pure AI processing without hardware"""
    print("\n🧠 DEMO 2: AI Processing Only (No Hardware)")
    print("=" * 50)
    
    try:
        from ai import AIProcessor
        
        print("🧠 Initializing AI processor...")
        ai = AIProcessor()
        
        if not ai.is_available():
            print("⚠️  AI not available - need OpenAI API key")
            return
        
        print("💬 Testing AI responses...")
        test_inputs = [
            "Hello, who are you?",
            "Can you dance for me?",
            "I'm feeling sad today",
            "Tell me a joke",
            "What can you do?"
        ]
        
        for user_input in test_inputs:
            print(f"\n👤 User: {user_input}")
            
            # Analyze input
            analysis = ai.analyze_input(user_input)
            print(f"🔍 Analysis: {analysis.get('intent', 'unknown')} (confidence: {analysis.get('confidence', 0):.2f})")
            
            # Generate response
            response = ai.generate_response(user_input)
            print(f"🤖 WORM: {response.text}")
            
            if response.emotion:
                print(f"😊 Emotion detected: {response.emotion}")
            if response.movement_hint:
                print(f"💃 Movement suggested: {response.movement_hint}")
            
            time.sleep(1)
        
        ai.close()
        print("\n✅ AI demo complete!")
        
    except Exception as e:
        print(f"❌ AI demo error: {e}")

def demo_config_only():
    """Demo: Configuration management without AI or hardware"""
    print("\n⚙️ DEMO 3: Configuration Management Only")
    print("=" * 50)
    
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
    """Demo: Audio functionality without AI or hardware"""
    print("\n🎤 DEMO 4: Audio Control Only")
    print("=" * 50)
    
    try:
        from core import AudioController
        
        print("🔊 Initializing audio controller...")
        audio = AudioController()
        
        print("🗣️ Testing text-to-speech...")
        test_phrases = [
            "Hello! I'm testing the audio system.",
            "This is a modular architecture demo.",
            "Each component works independently!"
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

def demo_full_integration():
    """Demo: Full system integration"""
    print("\n🌟 DEMO 5: Full System Integration")
    print("=" * 50)
    
    try:
        from worm_system_refactored import WormSystem
        
        print("🚀 Initializing full WORM system...")
        worm = WormSystem()
        
        # Show system status
        stats = worm.get_system_stats()
        print("\n📊 System Status:")
        print(f"  🤖 Hardware: {'✅ Connected' if stats['hardware']['connected'] else '🤖 Simulation'}")
        print(f"  🧠 AI: {'✅ Available' if stats['ai']['available'] else '❌ Disabled'}")
        print(f"  ⚙️  Responses: {stats['config']['total_responses']} loaded")
        
        print("\n💬 Testing integrated responses...")
        test_inputs = [
            "hello worm",
            "can you dance",
            "tell me about yourself"
        ]
        
        for user_input in test_inputs:
            print(f"\n👤 Input: {user_input}")
            result = worm._process_input(user_input)
            print(f"📝 Response type: {result.get('type', 'unknown')}")
            time.sleep(2)
        
        worm.stop()
        print("\n✅ Full integration demo complete!")
        
    except Exception as e:
        print(f"❌ Integration demo error: {e}")

def main():
    """Run all demos"""
    print("🎯 WORM MODULAR ARCHITECTURE DEMONSTRATION")
    print("🎯" * 25)
    print("\nThis demo shows how each component works independently")
    print("and how they integrate together in the full system.\n")
    
    demos = [
        ("Hardware Only", demo_hardware_only),
        ("AI Only", demo_ai_only), 
        ("Configuration Only", demo_config_only),
        ("Audio Only", demo_audio_only),
        ("Full Integration", demo_full_integration)
    ]
    
    try:
        for i, (name, demo_func) in enumerate(demos, 1):
            print(f"\n{'='*60}")
            print(f"🎯 RUNNING DEMO {i}/5: {name}")
            print(f"{'='*60}")
            
            demo_func()
            
            if i < len(demos):
                input(f"\n⏸️  Press Enter to continue to next demo...")
        
        print(f"\n{'='*60}")
        print("🎉 ALL DEMOS COMPLETED!")
        print("🎉" * 20)
        print("\n🎯 Key Benefits Demonstrated:")
        print("  ✅ Each component works independently")
        print("  ✅ Clean separation of concerns")
        print("  ✅ Easy testing and development")
        print("  ✅ Graceful fallbacks when components unavailable")
        print("  ✅ Modular architecture enables easy swapping")
        print("\n🐛 Happy modular worming! 🤖")
        
    except KeyboardInterrupt:
        print("\n\n🛑 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 