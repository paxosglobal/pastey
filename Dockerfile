FROM python:3.6
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
# this is over-ridden by entrypoint.sh which uses gunicorn/uvloop:
CMD ["python", "server.py"]
