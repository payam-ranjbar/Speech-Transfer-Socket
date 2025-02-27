import asyncio
import json

import websockets
from audio_transcribe import run_recording

async def send_audio(websocket):
    print("🔗 Client connected!")

    await websocket.send("ping")
    loop = asyncio.get_event_loop()

    def sync_callback(word):
        asyncio.run_coroutine_threadsafe(send_word(word), loop)

    async def send_word(word):
        print("Sending:", word)
        await websocket.send(word)

    await loop.run_in_executor(None, run_recording, sync_callback)


async def main():
    async with websockets.serve(send_audio, "localhost", 8765):
        print("🚀 WebSocket server running on ws://localhost:8765")
        await asyncio.Future()  # Keep server running



if __name__ == "__main__":
    asyncio.run(main())

