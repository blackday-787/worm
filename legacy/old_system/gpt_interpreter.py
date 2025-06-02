import os
import openai

# Load the API key from environment
openai.api_key = os.environ.get("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY is not set in your environment.")

def parse_gpt_command(nl_command):
    """
    Sends a natural language command to GPT-4 and returns a JSON string
    specifying either a symbolic command or servo+angle JSON list.
    """
    prompt = f"""
You are a worm motor controller. Translate user instructions into one of:

1. A JSON array of servo movements like:
   [{{"servo": 0, "angle": 90}}]

2. Or a single string command from this exact list:
   b   → reset all servos
   fl  → tilt front left
   fr  → tilt front right
   bl  → tilt back left
   br  → tilt back right
   t   → choreographed talk
   m1  → open and close mouth
   om  → hold mouth open
   cm  → close mouth
   ta  → test all movements
   d   → dance

Always choose a symbolic command if it matches. Do not wrap strings in JSON. Output **only** the string or JSON list.

Translate the users command below into **either**:
1. A valid JSON list of servo commands
2. A single string command from the list above

User Command: {nl_command}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Translate user commands for the worm."},
                  {"role": "user", "content": prompt}],
        temperature=0
    )

    try:
        command_json = response["choices"][0]["message"]["content"].strip()
        return command_json
    except Exception as e:
        print("Error parsing GPT-4 output:", e)
        return None