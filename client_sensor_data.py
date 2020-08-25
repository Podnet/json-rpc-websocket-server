import asyncio
import sys
import time
import websockets
from jsonrpcclient.clients.websockets_client import WebSocketsClient
from loguru import logger


async def main():
    async with websockets.connect("ws://localhost:7000") as ws:

        # Sending request with correct device ID
        response = await WebSocketsClient(ws).request("verify_device", "esp32_aa")
        logger.info(f"Response: {response.data}")

        if response.data.result == "ok":
            logger.success("Device verified. Sending data now...")

            while True:
                response = await WebSocketsClient(ws).request(
                    "sensor_data",
                    [
                        0,
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7,
                        8,
                        9,
                        10,
                        11,
                        12,
                        13,
                        14,
                        15,
                        16,
                        17,
                        18,
                        19,
                        20,
                    ],
                )
                logger.info(f"Response: {response.data}")
                time.sleep(1)

        else:
            logger.error("Device verification failed. Exiting!")
            sys.exit(0)


try:
    asyncio.get_event_loop().run_until_complete(main())
except KeyboardInterrupt:
    logger.error("Keyboard Interrupt raised. Exiting.")
