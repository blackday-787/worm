import os
import openai

# Ensure the API key is loaded from your environment variable.
openai.api_key = os.environ.get("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY is not set in your environment.")

def interpret_command(nl_command):
    """
    Sends a natural language command to GPT-4 and returns a JSON string 
    specifying the servo number and angle.
    """
    prompt = (
        "You are a command interpreter for an animatronic worm. "
        "Translate the following natural language command into a JSON object "
        "with two keys: 'servo' (an integer between 0 and 4) and 'angle' (an integer between 0 and 180). "
        "For example, 'raise the worm's head' could be translated to {'servo': 0, 'angle': 90}.\n"
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
        return command_json  # This is a JSON string.
    except Exception as e:
        print("Error parsing GPT-4 output:", e)
        return None
