#!/usr/bin/env python

from modules.bpm import emulate_bpm_data
from modules.video import generate_frames
from modules.temp import read_temp
from modules.heartmonitor import read_frec

import asyncio
import websockets
import random
import json


async def video_feed(websocket):
    frame_rate = 30
    delay = 1 / frame_rate
    async for frame in generate_frames():
        await websocket.send(json.dumps({"frameData": frame, "type": "video"}))
        print("camera data sent")
        await asyncio.sleep(delay)

# ENVIO DE ALERTAS Y DATOS AL CLIENTE


async def frecuency_feed(websocket):
    async for frecuencia in read_frec():
        await websocket.send(json.dumps({"frecuencia_cardiaca": frecuencia, "type": "frecuencia"}))
        # acá se ponen los datos en el html11
        edad = 65
        frec_max = 220 - edad
        frec_min = 220 - (edad * 0.5)

        if frecuencia > frec_max:
            # Poner alerta
            await websocket.send(
                json.dumps({"taquicardia": True, "type": "alerta_taquicardia"})
            )
        elif frecuencia < frec_min:
            await websocket.send(
                json.dumps({"bradicardia": True, "type": "alerta_bradicardia"})
            )  # Poner alerta


async def temperature_feed(websocket):
    async for temperatura in read_temp():
        await websocket.send(json.dumps({"sensor_temperatura": temperatura, "type": "temperatura"}))

        if temperatura > 37:
            await websocket.send(
                json.dumps({"fiebre": True, "type": "alerta_fiebre"})
            )
        elif temperatura < 35:
            await websocket.send(
                json.dumps({"hipotermia": True, "type": "alerta_hipotermia"}))


async def read_sensor_data():
    async for read in emulate_bpm_data():
        yield read


# async def sensor_data_feed(websocket):
#     async for sensor_value in read_sensor_data():
#         await websocket.send(json.dumps({"sensorData": sensor_value, "type": "sensor"}))
#         # Check for a threshold and send a notification if met
#         if sensor_value > 80:
#             await websocket.send(
#                 json.dumps({"thresholdExceeded": True, "type": "threshold"})
#             )
#         print("sent sensor data")


async def handler(websocket, _):
    try:
        # Start streaming video frames and sensor data concurrently
        video_task = asyncio.create_task(video_feed(websocket))
        # sensor_task = asyncio.create_task(sensor_data_feed(websocket))
        heartmonitor_task = asyncio.create_task(frecuency_feed(websocket))
        temp_task = asyncio.create_task(temperature_feed(websocket))

        await asyncio.gather(video_task, heartmonitor_task, temp_task)
    except websockets.exceptions.ConnectionClosed:
        pass  # Connection closed by the client


async def main():
    async with websockets.serve(handler, "192.168.1.81", 8090):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
