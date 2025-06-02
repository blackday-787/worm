import openai
import json
import serial
import time

openai.api_key = os.getenv("OPENAI_API_KEY")

SERIAL_PORT = "/dev/cu.usbmodem101"  # Update this as needed
BAUD_RATE = 9600
arduino = serial.Serial(SERIAL_PORT, BAUD_RATE)
time.sleep(2)

def send_to_gpt(prompt):
    return openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "user", "content": prompt}],
        functions=[{
            "name": "control_motor",
            "parameters": {
                "type": "object",
                "properties": {
                    "servo": {"type": "integer"},
                    "angle": {"type": "integer"}
                },
                "required": ["servo", "angle"]
            }
        }],
        function_call="auto"
    )

def handle_gpt_response(response):
    message = response["choices"][0]["message"]
    if "function_call" in message:
        args = json.loads(message["function_call"]["arguments"])
        command = json.dumps(args)
        print("[MOTOR CMD]:", command)
        arduino.write((command + "\n").encode())
    else:
        print("[GPT]:", message.get("content", "[No response]"))