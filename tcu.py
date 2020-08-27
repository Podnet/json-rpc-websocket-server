#!/usr/bin/env python3
import json
import asyncio
import websockets
from jsonrpcclient.requests import Request
from jsonrpcclient.response import SuccessResponse

SERVER_URL = "ws://localhost:7000"

async def send_sensor_data(websocket):
    req = Request("sensor_data", values="[1,2,3,4,5,6,7,8,9,10]")
    await websocket.send(str(req))
    print("Msg sent")
    await asyncio.sleep(1)

async def recv_msg(websocket):
    while True:
        message = await websocket.recv()
        print(message)
        message = json.loads(message)

        if "method" in message and message["method"] == "get_data_packet":
            await asyncio.sleep(2)
            
            resp = SuccessResponse(jsonrpc="2.0", id=message["id"], result={"get_data_packet": "[1,2,3,4,5,6,7,8,9,10]"})

            await websocket.send(str(resp))
            print(f"Sent back a response for get_packet_data -> {str(resp)}")


async def handler():
    
    async with websockets.connect(SERVER_URL) as websocket:
        task1 = asyncio.create_task(send_sensor_data(websocket))
        task2 = asyncio.create_task(recv_msg(websocket))

        await task1
        await task2


asyncio.get_event_loop().run_until_complete(handler())