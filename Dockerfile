FROM python:3.10.12-slim

RUN pip install --upgrade pip
RUN apt update && apt install -y python3-dev build-essential