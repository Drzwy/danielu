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
