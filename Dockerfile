FROM python:3.8-buster

WORKDIR /tmp

COPY requirements.txt /tmp/
RUN pip3 install -r requirements.txt