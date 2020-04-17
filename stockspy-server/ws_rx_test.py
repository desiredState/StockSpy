import asyncio
import websockets
import json


async def rx():
    uri = "ws://127.0.0.1:8765"

    async with websockets.connect(uri) as websocket:
        while True:
            results = await websocket.recv()
            print(json.loads(results))
            await asyncio.sleep(10)

asyncio.get_event_loop().run_until_complete(rx())
