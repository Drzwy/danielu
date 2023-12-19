#!/usr/bin/env python

import asyncio
import websockets
import cv2
import base64
import random
import json

camera = cv2.VideoCapture(0)


async def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode(".jpg", frame)
            frame_data = base64.b64encode(buffer).decode("utf-8")
            yield frame_data


async def video_feed(websocket):
    frame_rate = 30  # Adjust the frame rate as needed
    delay = 1 / frame_rate
    async for frame in generate_frames():
        await websocket.send(json.dumps({"frameData": frame, "type": "video"}))
        print("camera data sent")
        await asyncio.sleep(delay)


async def read_sensor_data():
    while True:
        # Replace this with actual sensor reading logic
        sensor_value = random.uniform(0, 100)
        await asyncio.sleep(0.2)  # Simulate sensor data being updated every second
        yield sensor_value


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
