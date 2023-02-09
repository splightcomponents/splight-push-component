FROM python:3.10-slim
COPY entrypoint.py /entrypoint.py
RUN pip install splight-cli
ENTRYPOINT ["/entrypoint.py"]
