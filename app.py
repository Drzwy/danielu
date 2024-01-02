#!/usr/bin/env python

# from modules.emulate_bpm import emulate_bpm_data
from modules.video import generate_frames
# from modules.temp import read_temp
# from modules.heartmonitor import read_frec
from modules.bpm import read_bpm
from modules.arduino.serialconnection import *

import asyncio
import websockets
import json


class InputChunkProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        print('data received', repr(data))
        if self.ws:
            self.ws.send(json.dumps({'bpm': data, "type": "bpm"}))

    def pause_reading(self):
        # This will stop the callbacks to data_received
        self.transport.pause_reading()

    def resume_reading(self):
        # This will start the callbacks to data_received again with all data that has been received in the meantime.
        self.transport.resume_reading()

    def set_websocket(self, websocket):
        self.ws = websocket


async def bpm_feed(websocket):
    setted = False
    paused = False
    protocol: InputChunkProtocol

    while True:
        if not setted:
            try:
                serialCoroutine = serial_asyncio.create_serial_connection(
                    asyncio.get_running_loop(),
                    InputChunkProtocol,
                    PORT,
                    BAUD_RATE,
                    timeout=1
                )
                _, protocol = await serialCoroutine
            except:
                print('error connecting')
                return
            protocol.set_websocket(websocket)
            setted = True
        elif active["bpm"] and setted and paused:
            protocol.resume_reading()
        elif not active["bpm"] and setted and not paused:
            protocol.pause_reading()
        else:
            pass


async def video_feed(websocket):
    frame_rate = 30
    delay = 1 / frame_rate

    while active["video"]:
        frame = await generate_frames()
        await websocket.send(json.dumps({"frameData": frame, "type": "video"}))
        print("camera data sent")
        await asyncio.sleep(delay)


active = {'bpm': False, 'video': False}


async def handler(websocket, _):
    initialized = False

    if not initialized:
        video_task = asyncio.create_task(
            video_feed(websocket))

        heartmonitor_task = asyncio.create_task(
            bpm_feed(websocket))

    # done, pending =  await asyncio.wait(
    #     [video_task, heartmonitor_task],
    #     return_when=asyncio.FIRST_COMPLETED
    # )
    # for task in pending:
    #     task.cancel()
    await asyncio.gather(video_task, heartmonitor_task)

    order = await websocket.recv()
    print(f'{order}: {type(order)}')

    if active["bpm"] and order == 'close_bpm':
        active["bpm"] = False
    elif not active['bpm'] and order == 'open_bpm':
        active["bpm"] = True
    elif active["video"] and order == 'close_video':
        active["video"] = False
    elif not active['video'] and order == 'open_video':
        active["video"] = True
    ...


async def main():
    async with websockets.serve(handler, "192.168.175.124", 8090):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    try:
        PORT = find_arduino_port()
        BAUD_RATE = 9600
    except IOError:
        print("error connecting")
    except:
        print("error ")
    asyncio.run(main())
