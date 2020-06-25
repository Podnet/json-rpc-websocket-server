import asyncio

import websockets
from loguru import logger
from jsonrpcclient.clients.websockets_client import WebSocketsClient


async def main():
    async with websockets.connect("ws://localhost:5000") as ws:

        # Sending request with correct device ID
        response = await WebSocketsClient(ws).request("verify_device", "esp32_aa")
        logger.info(f"Response: {response.data}")

        # Sending request with incorrect device ID
        response = await WebSocketsClient(ws).request("verify_device", "esp8266_ab765a")
        logger.info(f"Response: {response.data}")


asyncio.get_event_loop().run_until_complete(main())
