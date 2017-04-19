FROM python:3.6
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
# this is over-ridden by the `gunicorn.sh` entrypoint which uses gunicorn/uvloop:
CMD ["python", "server.py"]
