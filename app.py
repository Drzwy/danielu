#!/usr/bin/env python

import asyncio
import websockets
import random
import json

import sys

sys.path.append("/modules")

from modules.video import generate_frames
from modules.bpm import emulate_bpm_data


async def video_feed(websocket):
    frame_rate = 30
    delay = 1 / frame_rate
    async for frame in generate_frames():
        await websocket.send(json.dumps({"frameData": frame, "type": "video"}))
        print("camera data sent")
        await asyncio.sleep(delay)


async def read_sensor_data():
    async for read in emulate_bpm_data():
        yield read


async def sensor_data_feed(websocket):
    async for sensor_value in read_sensor_data():
        await websocket.send(json.dumps({"sensorData": sensor_value, "type": "sensor"}))
        # Check for a threshold and send a notification if met
        if sensor_value > 80:
            await websocket.send(
                json.dumps({"thresholdExceeded": True, "type": "threshold"})
            )
        print("sent sensor data")


async def handler(websocket, _):
    try:
        # Start streaming video frames and sensor data concurrently
        video_task = asyncio.create_task(video_feed(websocket))
        sensor_task = asyncio.create_task(sensor_data_feed(websocket))

        # Wait for either task to finish (e.g., if the WebSocket connection is closed)
        await asyncio.gather(video_task, sensor_task)
    except websockets.exceptions.ConnectionClosed:
        pass  # Connection closed by the client


async def main():
    async with websockets.serve(handler, "192.168.1.81", 8090):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
