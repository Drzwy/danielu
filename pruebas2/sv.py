import asyncio
import json
import websockets
import socket

from modules.video import generate_frames


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


print(get_ip())


async def video_feed(websocket):
    frame_rate = 30
    delay = 1 / frame_rate

    while active["video"]:
        frame = await generate_frames()
        await websocket.send(json.dumps({"frameData": frame, "type": "video"}))
        print("camera data sent")
        await asyncio.sleep(delay)

    print('stopped video')
    return True


async def bpm_feed(websocket):
    
    pass

active = {'bmp': False, 'video': False}


async def handler(websocket, _):
    async for order in websocket:
        print(f'{order}: {type(order)}')

        if order == 'open_camera':
            active['video'] = True
            asyncio.run(video_feed(websocket))
        elif order == 'close_camera':
            active['video'] = False
        elif order == 'open_bpm':
            active['bmp'] = True
            asyncio.run(bpm_feed(websocket))
        elif order == 'close_bpm':
            active['bmp'] = False


async def main():
    async with websockets.serve(handler, IP, PORT):
        await asyncio.Future()


if __name__ == "__main__":
    IP = get_ip()
    PORT = 8090

    asyncio.run(main())
