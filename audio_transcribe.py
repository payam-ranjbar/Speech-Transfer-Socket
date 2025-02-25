import sys
from vosk import Model, KaldiRecognizer
import pyaudio
import json
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
vosk_model = os.getenv("MODEL_PATH")

model = Model(vosk_model)
recognizer = KaldiRecognizer(model, 16000)

if not vosk_model:
    print("MODEL_PATH is not set in .env file.")
    sys.exit(1)


def list_microphones():
    mic = pyaudio.PyAudio()
    print("🎤 Available Microphones:")
    for i in range(mic.get_device_count()):
        device_info = mic.get_device_info_by_index(i)
        print(f"[{i}] {device_info['name']}")
    mic.terminate()


def choose_microphone():
    list_microphones()
    try:
        device_index = int(input("🎤 Enter the index of your preferred microphone: "))
        return device_index
    except ValueError:
        print("❌ Invalid input. Defaulting to system default microphone.")
        return None


def start_microphone(device_index=1):
    mic = pyaudio.PyAudio()

    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True,
                      input_device_index=device_index, frames_per_buffer=1000)

    stream.start_stream()
    print(f"✅ Using microphone: {mic.get_device_info_by_index(device_index)['name']}")
    return stream, mic

def read_stream(stream, mic, callback):
    last_word = ""
    try:
        while True:
            data = stream.read(4000, exception_on_overflow=False)
            recognizer.AcceptWaveform(data)
            partial_result = json.loads(recognizer.PartialResult())["partial"]

            if partial_result.strip():
                words = partial_result.split()
                if words:
                    new_word = words[-1]
                    if new_word != last_word:
                        callback(new_word)
                        last_word = new_word

    except KeyboardInterrupt:
        print("\n🚫 Stopping speech recognition.")
        stream.stop_stream()
        stream.close()
        mic.terminate()


def run_recording(callback):
    stream, mic = start_microphone()
    read_stream(stream, mic, callback)

async def print_partial_results(results):
    print("\r " + results)
    await asyncio.sleep(0)  # Yield control to the event loop

async def run_local():
    await run_recording(print_partial_results)
if __name__ == "__main__":
    asyncio.run(run_local())
