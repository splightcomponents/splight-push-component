FROM python:3-slim AS builder
COPY main.py /main,py
ENTRYPOINT ["/entrypoint.py"]


