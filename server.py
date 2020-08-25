#!/usr/bin/env python3
import asyncio
import json
import zmq
import zmq.asyncio

ctx = zmq.asyncio.Context()

import pyfiglet
import websockets
from loguru import logger
from jsonrpcserver import method, async_dispatch as dispatch

logger.add("server_datalog_{time}.log")

# Print the banner
print(pyfiglet.figlet_format("W S Server", font="slant"))

VERIFIED_DEVICES = ["esp32_aa"]
PORT = 7000

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
@method
async def verify_device(device_id):
    if device_id in VERIFIED_DEVICES:
        # generate a unique token here and return it to the user
        return "ok"
    else:
        return "invalid"


# Accepting sensor data from device
@method
async def sensor_data(data_points):

    logger.success(f"Processing data packet -> {data_points}")

    # logger.success(f"Processing data point generated on device at {timestamp} with data -> {data_points}")

    # Do some processing on `data_points` here

    # Return the timestamp of the received msg to let the device know that 
    # the server has processed the data.
    # return str(timestamp)

    return "some-timestamp"


# For cleaning incoming data from client
def clean_data(message):
    obj = json.loads(message)
    if not "jsonrpc" in obj:

        # Add JSON RPC key to data
        obj["jsonrpc"] = "2.0"

        # Delete 'src' key from data
        del obj["src"]

    return json.dumps(obj)


async def comcon_task():
    # Listen to incoming data on ZMQ Socket
    # Do something when you rx the data
    # Otherwise just pass
    zmq_sock = ctx.socket(zmq.REP)
    zmq_sock.bind("tcp://127.0.0.1:4444")

    while True:
        message = await zmq_sock.recv()
        print(f"Received msg from zmq -> {message}")

        await asyncio.sleep(3)
        
        print("Sending reply back to comcon.")
        await zmq_sock.send(b"msg-rx")



async def ws_loop(websocket, path):
    bg_task = asyncio.create_task(comcon_task())

    try:

        # Iterate through incoming msgs, and keep existing connections open
        async for message in websocket:

            # Clean the msg and log it
            logger.debug(f"Message: {message}")
            cleaned_data = clean_data(message)

            # Creating response
            response = await dispatch(cleaned_data)

            if not response.wanted:
                logger.info("Response not wanted by client")

            # Respond to the client, if required
            if response.wanted:
                logger.debug(f"Response: {response}")
                await websocket.send(str(response))
                logger.success("Response sent")

    except websockets.exceptions.ConnectionClosedError as e:
        logger.error("Connection closed unexpectedly")
        logger.debug(str(e))
    
    await bg_task


start_server = websockets.serve(
    ws_loop, "0.0.0.0", PORT, ping_interval=None, ping_timeout=None
)
asyncio.get_event_loop().run_until_complete(start_server)
logger.info(f"Listening for incoming connections on port {PORT}")


try:
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    logger.error("Keyboard Interrupt raised. Exiting.")
