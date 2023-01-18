FROM python:3.10-slim
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./trytytkowy_komunikator ./
COPY requirements.txt /app/requirements.txt
RUN ["pip", "install", "-r", "requirements.txt"]

COPY . /app