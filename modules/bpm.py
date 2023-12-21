from modules.arduino.serialconnection import is_valid_data, SerialProtocol

async def read_bpm(arduino: SerialProtocol):
    
    while True:
        read = is_valid_data(arduino.data)
        # SerialProtocol.data_received()

        if not read:
            continue

        yield read
        arduino.clear_data()
    
    
