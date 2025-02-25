import asyncio
import json

import websockets
from audio_transcribe import run_recording

connected_clients = {}
async def send_audio(websocket):
    print("🔗 Client connected!")

    try:
        message = await websocket.recv()
        target_words = json.loads(message)
        print(f"🎯 Listening for: {target_words}")

        connected_clients[websocket] = set(target_words)

        async def send_word(word):
            if word in connected_clients[websocket]:
                print("sending: ", word)
                await websocket.send(word)  # <-- Ensure send_word() is awaited properly

        await run_recording(send_word)  # <-- Await async function

    except websockets.exceptions.ConnectionClosed:
        print("❌ Client disconnected.")
        connected_clients.pop(websocket, None)


async def main():
    async with websockets.serve(send_audio, "localhost", 8765):
        print("🚀 WebSocket server running on ws://localhost:8765")
        await asyncio.Future()  # Keep server running


asyncio.run(main())
