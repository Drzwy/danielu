from arduino.serialconnection import find_arduino_port, connect_to_arduino, is_valid_data


PORT = find_arduino_port()
BAUD_RATE = 9600


async def read_bpm():
    try:
        arduino = connect_to_arduino(PORT, BAUD_RATE)
        while True:
            read = is_valid_data(arduino.readline())

            if not read:
                continue

            yield read
    except:
        print('error connecting')
    finally:
        if arduino.is_open:
            arduino.close()
            print("Serial connection closed")
