FROM python:3.10-slim
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#COPY ./trytytkowy_komunikator ./
COPY requirements.txt /app/requirements.txt
RUN ["pip", "install", "-r", "requirements.txt"]
RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "netcat"]

COPY . /app
