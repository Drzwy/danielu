from gpiozero import InputDevice

SENSOR_TEMP = InputDevice(1)

async def read_temp():
    while True:
        datos = SENSOR_TEMP.read_value()
        ### edad proviene del tipo paciente
        ### https://www.healthline.com/health/es/cual-es-el-rango-normal-de-la-temperatura-corporal#rango-de-temperatura
        yield datos