#!/usr/bin/env python3

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
        print(await websocket.recv())


async def handler():
    
    async with websockets.connect(SERVER_URL) as websocket:
        task1 = asyncio.create_task(send_sensor_data(websocket))
        task2 = asyncio.create_task(recv_msg(websocket))

        await task1
        await task2


asyncio.get_event_loop().run_until_complete(handler())