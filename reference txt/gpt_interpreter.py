import os
import openai

# Ensure the API key is loaded from your environment variable.
openai.api_key = os.environ.get("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY is not set in your environment.")

def load_context():
    try:
        with open("worm_prompt.txt", "r") as file:
            return file.read()
    except Exception as e:
        print("Error loading worm_prompt.txt:", e)
        return ""

def interpret_command(nl_command):
    """
    Sends a natural language command to GPT-4 and returns a JSON string 
    specifying the motor identifier (e.g., 'M0') and number of steps to rotate.
    """
    prompt_context = load_context()
    prompt = (
        f"{prompt_context}\n\n"
        "You are a command interpreter for a stepper motor-driven animatronic worm. "
        "Translate the following natural language command into a JSON object "
        "with two keys: 'motor' (a string such as 'M0' through 'M4') and 'steps' (an integer number of steps to move). "
        "For example, 'make the worm nod' could be translated to [{'motor': 'M0', 'steps': 512}].\n"
        f"Command: {nl_command}\n"
        "Output:"
    )
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    
    try:
        command_json = response["choices"][0]["message"]["content"].strip()
        return command_json
    except Exception as e:
        print("Error parsing GPT-4 output:", e)
        return None