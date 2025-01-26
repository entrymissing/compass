FROM python:3.9-slim-buster

WORKDIR /app

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

RUN python -m pip install --upgrade pip

COPY ./requirements.txt /app/requirements.txt
RUN python3 -m pip install -r /app/requirements.txt

COPY . /app

CMD gunicorn app:app -w 2 --threads 2 -b 0.0.0.0:80
