FROM python:3.10-slim
COPY entrypoint.py /entrypoint.py
RUN find . -name spec.json -print
RUN find . -name spec.json -print | head -n 1 | xargs grep '"splight_cli_version"' | grep  -Eo "[0-9](\.[0-9])*(\.dev[0-9])?" | xargs -I{} pip install splight-cli=={}
ENTRYPOINT ["/entrypoint.py"]
