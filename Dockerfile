FROM python:3.10-slim
COPY main.py /main.py
CMD ["/app/main.py"]