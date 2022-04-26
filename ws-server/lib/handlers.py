import aiohttp
from aiohttp import web
from lib.tasks import clear_task, send_wait_payload, HISTORY, create_task
from lib.ws import add_client, remove_client


def manual_mode_handler(_):
    mode = 'manual_mode'
    create_task(mode)
    return web.Response(text="clock mode starter")


def timer_mode_handler(_):
    mode = 'timer_mode'
    create_task(mode, preserved_mode='manual_mode')
    return web.Response(text="timer mode starter")


def stop_handler(_):
    clear_task()
    create_task('wait_mode')
    return web.Response(text='stop')


def history_handler(_):
    return web.json_response(list([p.to_dict() for p in HISTORY]))


async def websocket_handler(request):
    ws = web.WebSocketResponse(heartbeat=10)
    await ws.prepare(request)
    add_client(ws)
    try:
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('ws connection closed with exception %s' %
                      ws.exception())
    finally:
        remove_client(ws)

    print('websocket connection closed')
    return ws
