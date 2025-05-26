ef get_text_input():
    try:
        return input("[TEXT MODE] Type a message for the worm: ")
    except KeyboardInterrupt:
        print("\n[WORM] Goodbye.")
        return None