import queue
import sys
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer

q = queue.Queue()
model = Model("model")  # Make sure your Vosk model is downloaded to a folder named 'model'
samplerate = 16000
rec = KaldiRecognizer(model, samplerate)

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def get_speech_input():
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16', channels=1, callback=callback):
        print("[VOICE MODE] Speak now...")
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                return result.get("text", "")