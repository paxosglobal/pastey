FROM python:3.6
RUN mkdir /pip /code
WORKDIR /pip
ADD requirements.txt /pip
RUN pip install -r requirements.txt
WORKDIR /code

# this is over-ridden by the `gunicorn.sh` entrypoint which uses gunicorn/uvloop:
CMD ["python", "server.py"]
