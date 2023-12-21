# import serial
# import time

# # Configuración del puerto serie
# ser = serial.Serial('/dev/ttyUSB0', 115200)  # Ajusta el nombre del puerto según sea necesario

# try:
#     while True:
#         # Leer datos del puerto serie
#         line = ser.readline().decode('utf-8').strip()
#         print(f"Valor del sensor: {line}")

#         # Puedes realizar más procesamiento o almacenamiento según tus necesidades

#         time.sleep(1)  # Puedes ajustar el tiempo de espera según sea necesario

# except KeyboardInterrupt:
#     # Manejar una interrupción del teclado (Ctrl+C)
#     ser.close()

# # ----------------------

# import asyncio
# import serial_asyncio

# async def read_from_serial(serial):
#     while True:
#         line = await serial.read_until(b'\n').decode('utf-8').strip()
#         print(f"Valor del sensor: {line}")
#         # Puedes realizar más procesamiento o almacenamiento según tus necesidades

# try:
#     loop = asyncio.get_event_loop()

#     # Configuración del puerto serie
#     ser = serial_asyncio.create_serial_connection(loop, lambda: serial_asyncio.SerialTransport(), '/dev/ttyUSB0', baudrate=9600)

#     loop.run_until_complete(read_from_serial(ser[0]))

# except KeyboardInterrupt:
#     # Manejar una interrupción del teclado (Ctrl+C)
#     ser[0].close()
#     loop.close()

from serial.tools.list_ports import comports
import serial_asyncio
import asyncio
import time
import math


def find_arduino_port():
    arduino_ports = [
        p.device
        for p in comports()
        if 'ttyACM0' in p.description  # Adjust this based on your Arduino's description
    ]
    print(arduino_ports)
    if not arduino_ports:
        raise IOError("No Arduino found")
    if len(arduino_ports) > 1:
        print("Multiple Arduinos found - using the first one")
    return arduino_ports[0]

class SerialProtocol(asyncio.Protocol):
    def __init__(self):
        self.data = b""
    
    def connection_made(self, transport):
        print("Serial connection established.")
        self.transport = transport

    def data_received(self, data):
        print(f"Received: {data.decode()}")
        self.data += data
        
    def clear_data(self):
        self.data = b""

    def connection_lost(self, exc):
        print("Serial connection closed.")

async def connect_to_arduino(port, baud_rate):
    serialConnection = serial_asyncio.create_serial_connection(
        asyncio.get_event_loop(),
        SerialProtocol,
        port, baud_rate, timeout=1
    )
    return serialConnection


def is_valid_data(data):
    try:
        decoded_data = data.decode('utf-8')
        value = decoded_data
        print("caca: "+value)
        return value
    except (UnicodeDecodeError, ValueError):
        return False  # Los datos no son válidos o no se pueden decodificar como un entero


if __name__ == "__main__":
    pass
    # try:
    #     arduino_port = find_arduino_port()
    #     print(f"Arduino found on port: {arduino_port}")
    #     arduino = connect_to_arduino(arduino_port, 9600)
    #     print('este es el arduino: ', arduino.read)

    #     try:
    #         readCount = 0
    #         mean = 64
    #         while True:
    #             read = is_valid_data(arduino.readline())
    #             readCount += 1

    #             if not read:
    #                 # print('invalid data')
    #                 continue

    #             print(f"{readCount}: {read}")

    #             # time.sleep(0.02)  # Adjust the delay as needed.

    #     except KeyboardInterrupt:
    #         print("Program terminated manually")

    # finally:
    #     if arduino.is_open:
    #         arduino.close()
    #         print("Serial connection closed")
