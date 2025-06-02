# input_manager.py
import os

def get_input_mode():
    """
    Returns the current input mode: 'voice' or 'text'.
    Default is 'voice' if not set.
    """
    return os.getenv("WORM_INPUT_MODE", "voice").lower()