# Pastey: A Performant Async Python 3.6 App using Subconscoius

First, run a redis instance:
```bash
$  docker run -d -p 6379:6379 redis
```

Create & activate virtualenv (you may need to run `pip3 install virtualenv` if you haven't), install dependencies:
```bash
$ python3 -m virtualenv .venv && source .venv/bin/activate
$ pip3 install -r requirements.txt
```

Run the server:
```bash
$ python3.6 server.py
```

## TODOs
1. simple/performant deploy (docker?)
2. add test coverage!
3. make UI not awful?
4. performance test?
