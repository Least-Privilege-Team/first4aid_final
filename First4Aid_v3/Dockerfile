# syntax=docker/dockerfile:1
FROM python:3.11-rc-alpine
WORKDIR /code
RUN apk add build-base
RUN apk add g++
RUN apk add make
RUN apk add --update alpine-sdk
RUN apk update && apk add --virtual build-dependencies
RUN apk add python3-dev
RUN apk add libpq-dev
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 5000
COPY . .