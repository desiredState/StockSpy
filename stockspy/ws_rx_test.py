import asyncio
import websockets


async def rx():
    uri = "ws://127.0.0.1:8765"
    async with websockets.connect(uri) as websocket:
        results = await websocket.recv()
        print(results)

asyncio.get_event_loop().run_until_complete(rx())
