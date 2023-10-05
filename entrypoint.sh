echo $INPUT_SPLIGHT_CLI_VERSION
echo $SPLIGHT_CLI_VERSION

pip install splight-cli==$SPLIGHT_CLI_VERSION
python3 entrypoint.py