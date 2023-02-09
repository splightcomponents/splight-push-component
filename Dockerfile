FROM python:3.10-slim
COPY main.py /action/main.py
CMD ["python", "/action/main.py"]