from serial.tools.list_ports import comports
import serial
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

def connect_to_arduino(port, baud_rate):
    ser = serial.Serial(port, baud_rate, timeout=1)
    return ser

