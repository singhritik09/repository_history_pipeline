FROM python:3.8.10-slim

WORKDIR /app

COPY . /app/

RUN pip install requests


CMD ["python","index.py"]

