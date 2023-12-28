import asyncio
import math


class EmulationStopped(Exception):
    pass


async def emulate_bpm_data():
    """
    Emulates BPM data that slowly increases or decreases over time.

    Yields:
    - Simulated rounded BPM values.
    """
    START_BPM = 30
    END_BPM = 150
    HALF_PERIOD = 15  # Adjust the half period for one cycle (time to go up) in seconds
    SAMPLE_RATE = 10  # Adjust the sample rate (samples per second)

    # Calculate the frequency based on the half period
    frequency = 1 / (2 * HALF_PERIOD)

    try:
        while True:
            time_elapsed = 0
            while True:
                half = (START_BPM + END_BPM) / 2
                hdif = (END_BPM - START_BPM) / 2
                sine = math.sin(2 * math.pi * time_elapsed * frequency)
                bpm_value = round(half + hdif * sine)
                yield bpm_value
                time_elapsed += 1 / SAMPLE_RATE
                await asyncio.sleep(1 / SAMPLE_RATE)
                if time_elapsed >= HALF_PERIOD:
                    time_elapsed = (
                        0  # Restart the cycle after one complete cycle duration
                    )
    except asyncio.CancelledError:
        # asyncio.CancelledError is raised when the coroutine is cancelled
        pass
    except Exception as e:
        print(f"Error in emulate_bpm_data: {e}")
        raise


async def main():
    iterator = emulate_bpm_data().__aiter__()

    try:
        while True:
            read = await iterator.__anext__()
            print(f"BPM: {read} {type(read)}")
    except KeyboardInterrupt:
        print("Emulation stopped by user.")
    except StopAsyncIteration:
        print("Emulation stopped.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
