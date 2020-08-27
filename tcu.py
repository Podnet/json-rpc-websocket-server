#!/usr/bin/env python3

import asyncio
import websockets
from jsonrpcclient.requests import Request

SERVER_URL = "ws://localhost:7000"

async def hello():
    
    async with websockets.connect(SERVER_URL) as websocket:
        while True:
            req = Request("sensor_data", values="[1,2,3,4,5,6,7,8,9,10]")
            await websocket.send(str(req))
            print(await websocket.recv())
            await asyncio.sleep(1)

asyncio.get_event_loop().run_until_complete(hello())