FROM python:3.8.10-slim

WORKDIR /app

COPY . /app/

CMD ["python","index.py"]

