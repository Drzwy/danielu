from gpiozero import InputDevice

SENSOR_FREC_CARD = InputDevice(0)

async def read_frec():
    ## https://www.mayoclinic.org/es/healthy-lifestyle/fitness/in-depth/exercise-intensity/art-20046887
    while True:
        datos = SENSOR_FREC_CARD.read_value()
        yield datos