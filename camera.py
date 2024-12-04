import websockets
import asyncio
import signal
import os

async def echo(websocket):
    print("User connected to camera feed server")
    while True:
        message = await websocket.recv()
        print(message)
        jsonString = json.loads(message)
        msg = toTwist(jsonString)

async def main_server(ip,stop):
    async with websockets.serve(echo,'0.0.0.0',8766):
        print("camera server is listening on " + str(ip) + ":8766")
        await stop
    print('server stopped')

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGINT, stop.set_result, None)
    await asyncio.run(main_server(ip,stop))
