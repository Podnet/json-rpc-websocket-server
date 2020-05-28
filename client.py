import asyncio
import websockets
from jsonrpcclient.clients.websockets_client import WebSocketsClient

async def main():
    async with websockets.connect('ws://localhost:5000') as ws:
        response = await WebSocketsClient(ws).request('ping')
        print(response)

asyncio.get_event_loop().run_until_complete(main())
