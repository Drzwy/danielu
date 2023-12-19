from gpiozero import InputDevice
import time
import random
import asyncio
import json 

# sensores
SENSOR_FREC_CARD = InputDevice(0)
SENSOR_TEMP = InputDevice(1)



# LECTURA DE LOS SENSORES
async def read_temp():
    while True:
        datos = SENSOR_TEMP.read_value()
        ### edad proviene del tipo paciente
        ### https://www.healthline.com/health/es/cual-es-el-rango-normal-de-la-temperatura-corporal#rango-de-temperatura
        yield datos

async def read_frec():
    ## https://www.mayoclinic.org/es/healthy-lifestyle/fitness/in-depth/exercise-intensity/art-20046887
    while True:
        datos = SENSOR_FREC_CARD.read_value()
        yield datos


# ENVIO DE ALERTAS Y DATOS AL CLIENTE
async def frecuency_feed(websocket):
        async for frecuencia in read_frec():
            await websocket.send(json.dumps({"frecuencia_cardiaca": frecuencia, "type": "frecuencia"}))
            ## acá se ponen los datos en el html
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
                )# Poner alerta
                
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