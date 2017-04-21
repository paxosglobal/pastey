FROM python:3.6-alpine
RUN mkdir /pip /code
WORKDIR /pip
ADD requirements.txt /pip
RUN apk add --no-cache --virtual build-dependencies gcc musl-dev make
RUN pip install -r requirements.txt && apk del build-dependencies
WORKDIR /code

# this is over-ridden by the `gunicorn.sh` entrypoint which uses gunicorn/uvloop:
CMD ["python", "server.py"]
