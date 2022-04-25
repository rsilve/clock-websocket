#!/usr/bin/env python

from lib.handlers import manual_mode_handler, timer_mode_handler, stop_handler, websocket_handler, history_handler
from aiohttp import web
import aiohttp_cors


def configure_cors(application):
    cors = aiohttp_cors.setup(application, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=False,
            expose_headers="*",
            allow_headers="*",
        )
    })
    for route in list(application.router.routes()):
        cors.add(route)


app = web.Application()
app.add_routes([
    web.get('/manual', manual_mode_handler),
    web.get('/timer', timer_mode_handler),
    web.get('/stop', stop_handler),
    web.get('/history', history_handler),
    web.get('/ws', websocket_handler),
])

configure_cors(app)

if __name__ == "__main__":
    web.run_app(app)
