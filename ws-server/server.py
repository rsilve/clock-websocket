#!/usr/bin/env python
from datetime import datetime

import asyncio
from aiohttp import web

CLIENTS = set()
TASK = dict()


async def timer():
    while True:
        timestamp = datetime.now().isoformat()
        for ws in CLIENTS.copy():
            try:
                await ws.send_str(timestamp)
            except ConnectionResetError:
                CLIENTS.remove(ws)
                await ws.close()
        await asyncio.sleep(1)


def clear_task(preserved_mode = None):
    for task in TASK:
        if task != preserved_mode:
            TASK[task].cancel()
            del TASK[task]


async def timer_mode(request):
    clear_task('timer_mode')
    if 'timer_mode' not in TASK:
        TASK['timer_mode'] = asyncio.create_task(timer())
    return web.Response(text="Hello, world")


async def websocket_handler(request):
    ws = web.WebSocketResponse(heartbeat=10)
    await ws.prepare(request)
    CLIENTS.add(ws)

    async for _ in ws:
        await asyncio.Future()

    print('websocket connection closed')
    return ws


app = web.Application()
app.add_routes([web.get('/timer', timer_mode)])
app.add_routes([web.get('/ws', websocket_handler)])

if __name__ == "__main__":
    web.run_app(app)
