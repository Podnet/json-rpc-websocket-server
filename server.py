#!/usr/bin/env python3
import asyncio
import json
import zmq
import zmq.asyncio
import json


import pyfiglet
import websockets
from loguru import logger
from jsonrpcserver import method, async_dispatch as dispatch
from jsonrpcclient.requests import Request

logger.add("server_datalog_{time}.log")

# Print the banner
print(pyfiglet.figlet_format("W S Server", font="slant"))

VERIFIED_DEVICES = ["esp32_aa"]
ACTIVE_DEVICES = []
PORT = 7000

ctx = zmq.asyncio.Context()
zmq_sock = ctx.socket(zmq.REP)
zmq_url = "tcp://127.0.0.1:4444"
zmq_sock.bind(zmq_url)

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


async def comcon_task(websocket):

    while True:
        message = await zmq_sock.recv()
        message = message.decode('utf-8')
        message = json.loads(message)
        logger.info(f"Received a request from COMCON -> {message}")

        if message["method"] == "list":
            resp = json.dumps(ACTIVE_DEVICES)
            logger.info(f"Sending list of devices to COMCON. -> {resp}")
            await zmq_sock.send_string(resp)
        
        elif message["method"] == "get_data_packet":
            device_addr_index = int(message["params"]["device_addr_index"])
            device_addr = ACTIVE_DEVICES[device_addr_index]

            # Remove "device_addr_index" field
            del message["params"]["device_addr_index"]
            

            logger.info(f"{device_addr} -> {message}")
            
        
        else:
            await zmq_sock.send_string("unknown")



async def ws_loop(websocket, path):
    bg_task = asyncio.create_task(comcon_task(websocket))

    try:

        # Iterate through incoming msgs, and keep existing connections open
        async for message in websocket:

            # Insert device into ACTIVE_DEVICES list if it does not exists
            device_addr = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
            if device_addr not in ACTIVE_DEVICES:
                ACTIVE_DEVICES.append(device_addr)

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
    zmq_sock.unbind(zmq_url)
    logger.error("Keyboard Interrupt raised. Exiting.")
