import asyncio
import json

import pyfiglet
import websockets
from loguru import logger
from jsonrpcserver import method, async_dispatch as dispatch

# Print the banner
print(pyfiglet.figlet_format("W S Server", font="slant"))

VERIFIED_DEVICES = ["esp32_aa"]


@method
async def ping():
    logger.info("ping function executed")
    return "pong"


@method
async def test(param):
    logger.info("test function executed")
    logger.debug(f"test param: {param}")
    return f"ok"


# For verifying the end device
async def verify_device(device_id):
    if device_id in VERIFIED_DEVICES:
        return "ok"
    else:
        return "incorrect"


# Accepting sensor data from device
@method
async def sensor_data(data):
    logger.debug(data)
    return "ok"


# For cleaning incoming data from client
def clean_data(message):
    obj = json.loads(message)
    if not "jsonrpc" in obj:

        # Add JSON RPC key to data
        obj["jsonrpc"] = "2.0"

        # Delete 'src' key from data
        del obj["src"]

    return json.dumps(obj)


async def ws_loop(websocket, path):
    try:

        # Iterate through incoming msgs, and keep existing connections open
        async for message in websocket:

            # Clean the msg and log it
            logger.debug(f"Message: {message}")
            cleaned_data = clean_data(message)

            # Creating response
            response = await dispatch(cleaned_data)
            logger.debug(f"Response: {response}")

            # Respond to the client, if required
            if response.wanted:
                await websocket.send(str(response))
                logger.info("Response sent")

    except websockets.exceptions.ConnectionClosedError:
        logger.error("Connection closed unexpectedly")


start_server = websockets.serve(ws_loop, "0.0.0.0", 5000)
asyncio.get_event_loop().run_until_complete(start_server)
logger.info("Listening for incoming connections")

try:
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    logger.error("Keyboard Interrupt raised. Exiting.")
