from input_manager import get_input_mode
from text_input_mode import get_text_input
from speech_input_mode import get_speech_input
from output_handler import send_to_gpt, handle_gpt_response

def main():
    mode = get_input_mode()
    print(f"[WORM] Running in {mode.upper()} mode")

    while True:
        if mode == "text":
            user_input = get_text_input()
        else:
            user_input = get_speech_input()

        if not user_input:
            print("[WORM] No input detected. Exiting...")
            break

        response = send_to_gpt(user_input)
        handle_gpt_response(response)

if __name__ == "__main__":
    main()