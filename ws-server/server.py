#!/usr/bin/env python

import asyncio
import websockets
from datetime import datetime


async def handler(websocket):
    while True:
        try:
            await asyncio.sleep(1)
            timestamp = datetime.now().isoformat()
            await websocket.send(timestamp)
        except websockets.ConnectionClosedOK:
            break


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
