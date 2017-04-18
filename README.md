# Pastey: A Performant Async Python 3.6 App using Subconscious

## Quickstart

Install [docker](https://www.docker.com/community-edition) and then run:
```bash
$ docker-compose up
```

Visit this page in your browser:
http://0.0.0.0:5000/

## Slowstart

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

## Load Test

1. First, seed the database with a Pastey via web interface or curl call:
```bash
$ $ curl -F title="some title $(openssl rand -hex 12)" -F body="$(openssl rand -base64 1024)" 0.0.0.0:5000/pastes -L -s -o /dev/null -w '%{url_effective}'
http://0.0.0.0:5000/pastes/d1337110-2bcc-4e20-bc7e-87a6476a6b9
```

```bash
$ ab -n 10000 -c 10 http://0.0.0.0:5000/pastes/d1337110-2bcc-4e20-bc7e-87a6476a6b9

...

Concurrency Level:      10
Time taken for tests:   26.854 seconds
Complete requests:      10000
Failed requests:        0
Non-2xx responses:      10000
Total transferred:      1770000 bytes
HTML transferred:       100000 bytes
Requests per second:    372.38 [#/sec] (mean)
Time per request:       26.854 [ms] (mean)
Time per request:       2.685 [ms] (mean, across all concurrent requests)
Transfer rate:          64.37 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    2   2.5      1      23
Processing:     5   24   7.7     23     103
Waiting:        5   20   7.0     19     101
Total:          6   26   7.9     25     104

Percentage of the requests served within a certain time (ms)
  50%     25
  66%     27
  75%     29
  80%     30
  90%     34
  95%     38
  98%     45
  99%     54
 100%    104 (longest request)

```

## TODOs
1. add test coverage!
2. make UI not awful?
3. uvloop
