#!/usr/bin/env python3
"""Github action entry point script."""

import glob
import json
import logging
import os
import subprocess
from typing import Dict, List

from pydantic import BaseSettings

logging.basicConfig(level=logging.INFO)


class CLIConfig(BaseSettings):
    """Splight CLI configuration parameters."""

    SPLIGHT_ACCESS_ID: str
    SPLIGHT_SECRET_KEY: str
    SPLIGHT_PLATFORM_API_HOST: str = "https://api.splight-ai.com"

    class Config:
        """Splight config settings."""

        env_prefix = "INPUT_"


def configure_cli(config: Dict) -> None:
    """Load configuration to Splight CLI."""
    cmd = [
        "/usr/local/bin/splight",
        "configure",
        "--from-json",
        json.dumps(config),
    ]
    with subprocess.Popen(cmd, text=True) as p:
        _, error = p.communicate()
        if error:
            raise ChildProcessError(error)
    logging.info("Configuration successful.")


def push_component(path: str) -> None:
    """Push component using Splight CLI."""
    logging.info("Tring to push component at '%s' ...", path)
    cmd = ["/usr/local/bin/splight", "hub", "component", "push", path, "-f"]
    with subprocess.Popen(cmd, text=True) as p:
        _, error = p.communicate()
        if error:
            raise ChildProcessError(f"Error while pushing component: {error}")
    logging.info("Component at %s uploaded successfully.", path)


def find_files(expr: str) -> List:
    """Find files matching the given expression and return
    the parent directory of each one.
    """
    files = glob.glob(expr, recursive=True)
    return files


def install_splight_cli(spec_path: str):
    spec_dict = json.load(spec_path)
    version = spec_dict["splight_cli_version"]

    logging.info(f"Installing splight-cli {version}")
    cmd = ["/usr/bin/pip", "install", f"splight-cli=={version}"]
    with subprocess.Popen(cmd, text=True) as p:
        _, error = p.communicate()
        if error:
            raise ChildProcessError(
                f"Error while installing splight-cli: {error}"
            )


def main() -> None:
    """Main process."""
    config = CLIConfig()

    # I have to do this due to a bug in Github.
    # Missing parameters in Github actions are
    # passed as an empty string ("") instead
    # of preventing the environment variable
    # from being created.
    # It should be deleted when it gets fixed.
    # Issue: https://github.com/actions/runner/issues/924
    if not (config.SPLIGHT_ACCESS_ID and config.SPLIGHT_SECRET_KEY):
        raise ValueError("Missing splight secrets.")

    if config.SPLIGHT_PLATFORM_API_HOST == "":
        config.SPLIGHT_PLATFORM_API_HOST = "https://api.splight-ai.com"

    configure_cli(config.dict())

    files = find_files("./**/spec.json")
    if len(files) == 0:
        raise FileNotFoundError(
            "No 'spec.json' was found inside the repository."
        )
    logging.info("Found these components: %s", files)

    for spec_file in files:
        install_splight_cli(os.path.abspath(spec_file))
        push_component(os.path.dirname(os.path.abspath(spec_file)))


if __name__ == "__main__":
    main()
