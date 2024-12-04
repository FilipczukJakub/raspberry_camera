import websockets
import asyncio
import signal
import threading
import json
import os
from picamera2 import Picamera2, Preview
import time
global_stop = False

async def echo(websocket):
    global global_stop
    while not global_stop:
        await websocket.send()
        asyncio.sleep(0.2)

async def camera_feed():
    global global_stop
    picam2 = Picamera2()
    picam2.start_preview(Preview.QLGL)
    preview_config = picam2.create_preview_configuration()
    capture_config = picam2.create_preview_configuration()
    picam2.configure(capture_config)
    picam2.start()
    while not global_stop:
        image = picam2.capture_image()
        print(image)

async def server(ip,stop):
    async with websockets.serve(echo,'0.0.0.0',8766):
        print("Camera feed is beeing send")
        await stop
    print("Camera feed stopped")

async def main():
    global global_stop
    ip = os.getenv("HOST_IP")
    camera_feed_thread = threading.Thread(target=camera_feed,args=())
    camera_feed_thread.start()
    loop = asyncio.get_event_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGINT, stop.set_result, None)
    await server(ip,stop)
    global_stop = True
    print("Finish...")



if __name__ == "__main__":
    asyncio.run(main())
