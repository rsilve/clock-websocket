import json
from collections import deque
from datetime import datetime, timedelta
from random import randrange

import asyncio
from lib.models import Payload
from lib.ws import broadcast

TASK = dict()
HISTORY = deque(maxlen=10)


async def send_wait_payload():
    payload = Payload('wait_mode', None, None)
    payload_str = json.dumps(payload.to_dict())
    await broadcast(payload_str)


async def timer():
    start = datetime.now()
    try:
        current = start
        end = current + timedelta(seconds=10)
        while current < end:
            payload = Payload('timer_mode', current.isoformat(), start.isoformat(), end.isoformat())
            payload_str = json.dumps(payload.to_dict())
            await broadcast(payload_str)
            await asyncio.sleep(1)
            current = datetime.now()
        HISTORY.appendleft(Payload('timer_mode', current.isoformat(), start.isoformat(), end.isoformat()))
    except asyncio.CancelledError:
        HISTORY.appendleft(Payload('timer_mode', datetime.now().isoformat(), start.isoformat()))
        raise
    create_task('wait_mode', preserved_mode='manual_mode')


async def manual():
    start = datetime.now()
    try:
        while True:
            timestamp = datetime.now().isoformat()
            payload = Payload('manual_mode', timestamp, start.isoformat())
            payload_str = json.dumps(payload.to_dict())
            await broadcast(payload_str)
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        HISTORY.appendleft(Payload('manual_mode', datetime.now().isoformat(), start.isoformat()))
        raise


async def wait():
    while True:
        timestamp = datetime.now().isoformat()
        payload = Payload('wait_mode', timestamp, None)
        payload_str = json.dumps(payload.to_dict())
        await broadcast(payload_str)
        await asyncio.sleep(1)


def clear_task(current_mode=None, preserved_mode=None):
    for task in TASK.copy():
        if task != current_mode and task != preserved_mode and task != 'simulation':
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
            'wait_mode': wait,
        }[mode]
        TASK[mode] = asyncio.create_task(coroutine())


def simulation():
    async def coro():
        while True:
            await asyncio.sleep(20 + randrange(10))
            create_task('timer_mode', preserved_mode='manual_mode')

    TASK['simulation'] = asyncio.create_task(coro())

