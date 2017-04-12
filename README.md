# Pastey: An Example Performant Async Python 3.6 Redis-Backed App

Run a redis instance:
```bash
$  docker run -d -p 6379:6379 redis
```

Create & activate virtualenv (you may need to run `pip3 install virtualenv` if you haven't), install dependencies:
```bash
$ python3 -m virtualenv .venv && source .venv/bin/activate
$ pip3 install aiohttp aiohttp-jinja2 aioredis
$ pip3 install -e git+https://github.com/paxos-bankchain/subconscious.git@9bed39fd5523a6a36417abe5873773d3cb96ea25#egg=subconscious --no-dependencies
```
(FIXME: `--no-dependencies` and add subconscious to pypi)

Run the server:
```bash
$ python3 server.py
```

## TODOs
1. simple/performant deploy (docker?)
2. add test coverage!
3. make UI not awful?
4. load test?
