FROM python:3.6
RUN mkdir /pip
WORKDIR /pip
ADD requirements.txt /pip
RUN pip install -r requirements.txt
WORKDIR /code
ADD . /code

# this is over-ridden by the `gunicorn.sh` entrypoint which uses gunicorn/uvloop:
CMD ["python", "server.py"]
