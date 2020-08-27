#!/usr/bin/env python3
import json
import asyncio
import websockets
from jsonrpcclient.requests import Request

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
            
            data = {"values": "[1,2,3,4,5,6,7,8,9,10]"}

            await websocket.send(json.dumps(data))
            print("Sent back a response for get_packet_data")


async def handler():
    
    async with websockets.connect(SERVER_URL) as websocket:
        task1 = asyncio.create_task(send_sensor_data(websocket))
        task2 = asyncio.create_task(recv_msg(websocket))

        await task1
        await task2


asyncio.get_event_loop().run_until_complete(handler())