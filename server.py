import asyncio

import pyfiglet
import websockets
from jsonrpcserver import method
from loguru import logger

# Print the banner
print(pyfiglet.figlet_format("W S Server", font="slant"))

i = 0


@method
async def ping():
    print("Received a ping request")
    return "pong"


@method
async def test(a, b, c):
    print("Under test method")


async def ws_loop(websocket, path):
    try:
        async for message in websocket:
            logger.info(f"Received a msg from client: {message}")
            logger.debug(f"Message: {message}")
    except websockets.exceptions.ConnectionClosedError:
        logger.error("Connection closed unexpectedly")

    # global i
    # recv_data = await websocket.recv()
    # print(f"[{i}] Recv data: {recv_data}")
    # print(f"[{i}] Recv data type: {type(recv_data)}")
    # obj = json.loads(recv_data)
    # if not "jsonrpc" in obj:
    #     obj["jsonrpc"] = "2.0"
    #     del obj["src"]
    #     recv_data = json.dumps(obj)
    #     print(f"[{i}] Modified recv data: {recv_data}")
    # response = await dispatch(recv_data)
    # print(f"[{i}] Response: {response}")
    # i += 1

    # if not response.wanted:
    #     print("======================")

    # if response.wanted:
    #     print(f"[{i}] Sending back response")
    #     await websocket.send(str(response))
    #     print("======================")


start_server = websockets.serve(ws_loop, "0.0.0.0", 5000)
asyncio.get_event_loop().run_until_complete(start_server)
logger.info("Listening for incoming connections")

try:
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    logger.error("Keyboard Interrupt raised. Exiting.")
