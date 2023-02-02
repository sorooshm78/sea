FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app

RUN apk add g++ 
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
