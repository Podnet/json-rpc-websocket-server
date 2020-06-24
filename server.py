import asyncio
import websockets
from jsonrpcserver import method, async_dispatch as dispatch
import json

i = 0


@method
async def ping():
    print("Received a ping request")
    return "pong"


@method
async def test(a, b, c):
    print("Under test method")


async def main(websocket, path):

    async for message in websocket:
        print("####################")
        print(message)
        print(type(message))

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


start_server = websockets.serve(main, "0.0.0.0", 5000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
