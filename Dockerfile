FROM python:3.10-slim
RUN pip install pydantic==1.10.2
COPY entrypoint.py /entrypoint.py
ENTRYPOINT ["/entrypoint.py"]
