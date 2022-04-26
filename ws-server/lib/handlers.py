import aiohttp
from aiohttp import web
from lib.tasks import CLIENTS, clear_task, send_wait_payload, HISTORY, create_task


async def manual_mode_handler(_):
    mode = 'manual_mode'
    await create_task(mode)
    return web.Response(text="clock mode starter")


async def timer_mode_handler(_):
    mode = 'timer_mode'
    await create_task(mode, preserved_mode='manual_mode')
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
