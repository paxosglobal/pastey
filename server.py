#!/usr/bin/env python3

import os

from app import create_app
from aiohttp import web


if __name__ == '__main__':
    app = create_app()
    web.run_app(
        app,
        host=os.getenv('PASTEY_HOST', '0.0.0.0'),
        port=int(os.getenv('PASTEY_PORT', 5000)),
    )
