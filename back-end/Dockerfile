# syntax=docker/dockerfile:1
FROM python:3.9-alpine
WORKDIR /code
RUN apk add build-base
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 5000
COPY . .