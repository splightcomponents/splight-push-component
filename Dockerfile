FROM python:3.10-slim
COPY entrypoint.py /entrypoint.py
RUN echo $splight_cli_version && echo $SPLIGHT_CLI_VERSION
ARG SPLIGHT_CLI_VERSION
ENV SPLIGHT_CLI_VERSION=$SPLIGHT_CLI_VERSION
RUN pip install splight-cli==${SPLIGHT_CLI_VERSION}
ENTRYPOINT ["/entrypoint.py"]
