FROM python:3-slim AS builder
COPY entrypoint.py /entrypoint,py
ENTRYPOINT ["/entrypoint.py"]


