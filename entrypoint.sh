#!/usr/bin/env bash
gunicorn -w 1 --bind 0.0.0.0:5000 --log-level=info --worker-class aiohttp.worker.GunicornUVLoopWebWorker 'server:create_app()'
