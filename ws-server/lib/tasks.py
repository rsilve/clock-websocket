import json
from collections import deque
from datetime import datetime, timedelta

import asyncio
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


async def manual():
    start = datetime.now()
    try:
        while True:
            timestamp = datetime.now().isoformat()
            payload = Payload('manual_mode', timestamp, -1, start.isoformat())
            payload_str = json.dumps(payload.to_dict())
            for ws in CLIENTS.copy():
                try:
                    await ws.send_str(payload_str)
                except ConnectionResetError:
                    CLIENTS.remove(ws)
                    await ws.close()
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        HISTORY.appendleft(Payload('manual_mode', datetime.now().isoformat(), -1, start.isoformat()))
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

