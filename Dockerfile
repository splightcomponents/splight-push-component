FROM python:3.10-slim
COPY main.py /main.py
ENTRYPOINT ["/main.py"]