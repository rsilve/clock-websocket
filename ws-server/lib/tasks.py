import json
from collections import deque
from datetime import datetime, timedelta

import asyncio
from lib.models import Payload

CLIENTS = set()
TASK = dict()
HISTORY = deque(maxlen=10)


async def ws_send_str(payload_str):
    for ws in CLIENTS.copy():
        try:
            await ws.send_str(payload_str)
        except ConnectionResetError:
            CLIENTS.remove(ws)
            await ws.close()


async def send_wait_payload():
    payload = Payload('wait_mode', None, None)
    payload_str = json.dumps(payload.to_dict())
    await ws_send_str(payload_str)


async def timer():
    start = datetime.now()
    try:
        current = start
        end = current + timedelta(seconds=60)
        while current < end:
            payload = Payload('timer_mode', current.isoformat(), start.isoformat(), end.isoformat())
            payload_str = json.dumps(payload.to_dict())
            await ws_send_str(payload_str)
            await asyncio.sleep(1)
            current = datetime.now()
        HISTORY.appendleft(Payload('timer_mode', current.isoformat(), start.isoformat(), end.isoformat()))
        await send_wait_payload()
    except asyncio.CancelledError:
        HISTORY.appendleft(Payload('timer_mode', datetime.now().isoformat(), start.isoformat()))
        raise


async def manual():
    start = datetime.now()
    try:
        while True:
            timestamp = datetime.now().isoformat()
            payload = Payload('manual_mode', timestamp, start.isoformat())
            payload_str = json.dumps(payload.to_dict())
            await ws_send_str(payload_str)
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        HISTORY.appendleft(Payload('manual_mode', datetime.now().isoformat(), start.isoformat()))
        raise


def clear_task(current_mode=None, preserved_mode=None):
    for task in TASK.copy():
        if task != current_mode and task != preserved_mode:
            TASK[task].cancel()
            del TASK[task]


def create_task(mode, preserved_mode=None):
    clear_task(mode, preserved_mode)
    if preserved_mode in TASK:
        return
    if mode not in TASK:
        coroutine = {
            'manual_mode': manual,
            'timer_mode': timer,
        }[mode]
        TASK[mode] = asyncio.create_task(coroutine())
