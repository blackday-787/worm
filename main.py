import os
from get_text_input import get_text_input
from speech_input_mode import get_speech_input
from gpt_interpreter import parse_gpt_command
from output_handler import send_command_to_serial

def get_input_mode():
    mode = os.getenv("WORM_INPUT_MODE", "text")
    if mode == "voice":
        return get_speech_input
    else:
        return get_text_input

def main():
    print("🐛 WORM SYSTEM ONLINE")
    input_func = get_input_mode()

    while True:
        user_input = input_func()
        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit"]:
            print("👋 Exiting...")
            break

        print(f"> You said: {user_input}")

        gpt_output = parse_gpt_command(user_input)
        print(f"> GPT returned: {gpt_output}")

        send_command_to_serial(gpt_output)

if __name__ == "__main__":
    main()
