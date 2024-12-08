import websockets
import asyncio
import signal
import threading
import json
import os
from picamera2 import Picamera2, Preview
import time
from io import BytesIO
global_stop = False
image = None
async def echo(websocket):
    global global_stop
    global image
    print("connected")
    while not global_stop:
        try:
            local_image = image
            buffer = BytesIO()
            local_image.save(buffer, format='JPEG', quality=50)
            image_bytes = buffer.getvalue()
            buffer.close()
            await websocket.send(image_bytes)
            await asyncio.sleep(0.05)
        except:
            print("disconnected...")
            break

def camera_feed():
    global global_stop
    global image
    picam2 = Picamera2()
    picam2.start_preview(Preview.QTGL)
    preview_config = picam2.create_preview_configuration()
    capture_config = picam2.create_preview_configuration()
    picam2.configure(capture_config)
    picam2.start()
    while not global_stop:
        image = picam2.capture_image()
        time.sleep(0.05)

async def server(ip,stop):
    async with websockets.serve(echo,'0.0.0.0',8767):
        print("Camera feed is beeing send")
        await stop
    print("Camer a feed stopped")

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
