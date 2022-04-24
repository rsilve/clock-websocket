import json

import aiohttp
from aiohttp import web
from datetime import datetime, timedelta
import asyncio
from collections import deque

from lib.models import Payload

CLIENTS = set()
TASK = dict()
HISTORY = deque(maxlen=10)


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
    try:
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
        HISTORY.appendleft(Payload('timer_mode', current.isoformat(), -1, start.isoformat()))
        await send_wait_payload()
    except asyncio.CancelledError:
        HISTORY.appendleft(Payload('timer_mode', datetime.now().isoformat(), -1, start.isoformat()))
        raise


async def clock():
    start = datetime.now()
    try:
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
    except asyncio.CancelledError:
        HISTORY.appendleft(Payload('clock_mode', datetime.now().isoformat(), -1, start.isoformat()))
        raise


def clear_task(preserved_mode=None):
    for task in TASK.copy():
        if task != preserved_mode:
            TASK[task].cancel()
            del TASK[task]


async def clock_mode_handler(_):
    mode = 'clock_mode'
    clear_task(mode)
    if mode not in TASK:
        TASK[mode] = asyncio.create_task(clock())
    return web.Response(text="clock mode starter")


def timer_mode_handler(_):
    mode = 'timer_mode'
    clear_task(mode)
    if mode not in TASK:
        TASK[mode] = asyncio.create_task(timer())
    return web.Response(text="timer mode starter")


async def stop_handler(_):
    clear_task()
    await send_wait_payload()
    return web.Response(text='stop')


def history_handler(_):
    return web.json_response(list([p.to_dict() for p in HISTORY]))


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
