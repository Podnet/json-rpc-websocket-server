import asyncio

import websockets
from loguru import logger
from jsonrpcclient.clients.websockets_client import WebSocketsClient


async def main():
    async with websockets.connect("ws://localhost:5000") as ws:
        response = await WebSocketsClient(ws).request("ping")
        # await ws.send("ping")
        # response = await ws.recv()
        logger.info(f"Response: {response.data}")

        response = await WebSocketsClient(ws).request("test", {"a": 21, "b": 25})
        logger.info(f"Response: {response.data}")


asyncio.get_event_loop().run_until_complete(main())
