import asyncio
import websockets
from audio_transcribe import run_recording


async def send_audio(websocket, path):
    print("🔗 Client connected!")

    async def send_word(word):
        print("sending: ", word)
        await websocket.send(word)  # Send full words

    try:
        await asyncio.to_thread(run_recording, send_word)  # Run speech recognition in a separate thread
    except websockets.exceptions.ConnectionClosed:
        print("❌ Client disconnected.")


async def main():
    async with websockets.serve(send_audio, "localhost", 8765):
        print("🚀 WebSocket server running on ws://localhost:8765")
        await asyncio.Future()  # Keep server running


asyncio.run(main())
