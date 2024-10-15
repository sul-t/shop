FROM python:3.12.3-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

WORKDIR /shop

COPY requirements.txt req.txt
RUN pip install -r req.txt

# COPY db_managment.py db_managment.py
# RUN python3 db_managment.py

COPY db_connect.py db_managment.py main.py utils.py ./


