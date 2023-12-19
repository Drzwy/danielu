import asyncio
import json
import secrets

import websockets


CONNECTIONS = set()


async def consumer_handler(websocket):
    ...


async def producer_handler(websocket):
    ...


async def handler(websocket):
    CONNECTIONS.add(websocket)
    consumer_task = asyncio.create_task(consumer_handler(websocket))
    producer_task = asyncio.create_task(producer_handler(websocket))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()
    CONNECTIONS.remove(websocket)


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
