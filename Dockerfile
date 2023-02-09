FROM python:3.10-slim

ADD . /action
WORKDIR /action
CMD python main.py