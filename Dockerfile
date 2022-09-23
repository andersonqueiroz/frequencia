FROM python:3.10-slim

RUN apt-get update && apt-get install gcc python3-dev -y

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /code/

RUN chmod +x entrypoint.sh