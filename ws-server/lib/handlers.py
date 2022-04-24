import json

import aiohttp
from aiohttp import web
from datetime import datetime, timedelta
import asyncio

from lib.models import Payload

CLIENTS = set()
TASK = dict()


async def send_wait_payload():
    payload = Payload('wait_mode', None, -1, None)
    for ws in CLIENTS.copy():
        try:
            await ws.send_str(json.dumps(payload.to_dict()))
        except ConnectionResetError:
            CLIENTS.remove(ws)
            await ws.close()


async def timer():
    start = datetime.now()
    current = start
    end = current + timedelta(seconds=60)
    while current < end:
        current = datetime.now()
        payload = Payload('timer_mode', current.isoformat(), -1, start.isoformat())
        payload_str = json.dumps(payload.to_dict())
        for ws in CLIENTS.copy():
            try:
                await ws.send_str(payload_str)
            except ConnectionResetError:
                CLIENTS.remove(ws)
                await ws.close()
        await asyncio.sleep(1)
    await send_wait_payload()


async def clock():
    start = datetime.now()
    while True:
        timestamp = datetime.now().isoformat()
        payload = Payload('clock_mode', timestamp, -1, start.isoformat())
        payload_str = json.dumps(payload.to_dict())
        for ws in CLIENTS.copy():
            try:
                await ws.send_str(payload_str)
            except ConnectionResetError:
                CLIENTS.remove(ws)
                await ws.close()
        await asyncio.sleep(1)


def clear_task(preserved_mode=None):
    for task in TASK.copy():
        if task != preserved_mode:
            TASK[task].cancel()
            del TASK[task]


async def clock_mode_handler(_):
    clear_task('clock_mode')
    if 'clock_mode' not in TASK:
        TASK['clock_mode'] = asyncio.create_task(clock())
    print('clock_mode')
    return web.Response(text="Hello, world")


def timer_mode_handler(_):
    mode = 'timer_mode'
    clear_task(mode)
    if mode not in TASK:
        TASK[mode] = asyncio.create_task(timer())
    print('timer_mode')
    payload = Payload(mode, 'timestamp', -1, None)
    return web.json_response(payload.to_dict())


async def stop_handler(_):
    clear_task()
    await send_wait_payload()

    print('stop')
    return web.Response(text='stop')


async def websocket_handler(request):
    ws = web.WebSocketResponse(heartbeat=10)
    await ws.prepare(request)
    CLIENTS.add(ws)
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')
    return ws
