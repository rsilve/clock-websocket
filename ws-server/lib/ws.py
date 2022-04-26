from aiohttp import WSCloseCode

CLIENTS = set()


def add_client(ws):
    CLIENTS.add(ws)


def remove_client(ws):
    CLIENTS.remove(ws)


async def close_all_clients():
    for ws in CLIENTS.copy():
        await ws.close(code=WSCloseCode.GOING_AWAY,
                       message='Server shutdown')


async def broadcast(payload_str):
    for ws in CLIENTS.copy():
        try:
            await ws.send_str(payload_str)
        except ConnectionResetError:
            CLIENTS.remove(ws)
            await ws.close()
