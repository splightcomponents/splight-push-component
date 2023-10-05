FROM python:3.10-slim
COPY entrypoint.py /entrypoint.py
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
