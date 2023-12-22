import serial
import time

# Configuración del puerto serie
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Ajusta el nombre del puerto según sea necesario

try:
    while True:
        # Leer datos del puerto serie
        line = ser.readline().decode('utf-8').strip()
        print(f"Valor del sensor: {line}")

        # Puedes realizar más procesamiento o almacenamiento según tus necesidades

        time.sleep(1)  # Puedes ajustar el tiempo de espera según sea necesario

except KeyboardInterrupt:
    # Manejar una interrupción del teclado (Ctrl+C)
    ser.close()

# ----------------------

import asyncio
import serial_asyncio

async def read_from_serial(serial):
    while True:
        line = await serial.read_until(b'\n').decode('utf-8').strip()
        print(f"Valor del sensor: {line}")
        # Puedes realizar más procesamiento o almacenamiento según tus necesidades

try:
    loop = asyncio.get_event_loop()

    # Configuración del puerto serie
    ser = serial_asyncio.create_serial_connection(loop, lambda: serial_asyncio.SerialTransport(), '/dev/ttyUSB0', baudrate=9600)

    loop.run_until_complete(read_from_serial(ser[0]))

except KeyboardInterrupt:
    # Manejar una interrupción del teclado (Ctrl+C)
    ser[0].close()
    loop.close()
