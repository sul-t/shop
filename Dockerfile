FROM python:3.12.3-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

WORKDIR /shop

COPY requirements.txt req.txt
RUN pip install -r req.txt

COPY managment_db.py man_db.py
RUN python3 man_db.py

COPY main.py utils.py ./


