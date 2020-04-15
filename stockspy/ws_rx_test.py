import asyncio
import websockets
import json


async def rx():
    uri = "ws://127.0.0.1:8765"
    async with websockets.connect(uri) as websocket:
        results = await websocket.recv()
        print(json.loads(results))

asyncio.get_event_loop().run_until_complete(rx())
