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

1. First, seed the database with a bunch of Pasteys via curl call:
```bash
$ for i in {1..10}; do curl -F title="Title #$i" -F body="$(openssl rand -base64 1000)" 0.0.0.0:5000/pastes -L -s -o /dev/null -w '%{url_effective}\n'; done
http://0.0.0.0:5000/pastes/80f58d80-a6a3-4bf3-86d4-7ded65e41448
...
```
(you can do this via web interface if you prefer)

Make a bunch of requests to one valid Pastey URL:
```bash
$ ab -n 10000 -c 5 http://0.0.0.0:5000/pastes/80f58d80-a6a3-4bf3-86d4-7ded65e41448
...

Concurrency Level:      5
Time taken for tests:   40.628 seconds
Complete requests:      10000
Failed requests:        0
Total transferred:      24910000 bytes
HTML transferred:       23390000 bytes
Requests per second:    246.14 [#/sec] (mean)
Time per request:       20.314 [ms] (mean)
Time per request:       4.063 [ms] (mean, across all concurrent requests)
Transfer rate:          598.76 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    1   6.3      1     236
Processing:     5   18  27.7     16    1024
Waiting:        5   17  27.4     14    1019
Total:          6   19  28.4     17    1025

Percentage of the requests served within a certain time (ms)
  50%     17
  66%     18
  75%     19
  80%     19
  90%     22
  95%     26
  98%     33
  99%    116
 100%   1025 (longest request)
```

## TODOs
1. add test coverage!
2. make UI not awful?
