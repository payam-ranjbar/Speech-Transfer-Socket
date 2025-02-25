import sys
from vosk import Model, KaldiRecognizer
import pyaudio
import json
from dotenv import load_dotenv
import os

load_dotenv()
vosk_model = os.getenv("MODEL_PATH")

model = Model(vosk_model)
recognizer = KaldiRecognizer(model, 16000)

if not vosk_model:
    print("MODEL_PATH is not set in .env file.")
    sys.exit(1)


def start_microphone():
    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1000)
    stream.start_stream()
    return stream, mic


def read_stream(stream, mic):
    try:
        while True:
            data = stream.read(1000, exception_on_overflow=False)
            recognizer.AcceptWaveform(data)
            partial_result = json.loads(recognizer.PartialResult())["partial"]
            if partial_result.strip():
                sys.stdout.write("\r" + partial_result + " ")
                sys.stdout.flush()

    except KeyboardInterrupt:
        print("\n🚫 Stopping speech recognition.")
        stream.stop_stream()
        stream.close()
        mic.terminate()


def run_recording():
    stream, mic = start_microphone()
    read_stream(stream, mic)


if __name__ == "__main__":
    run_recording()
