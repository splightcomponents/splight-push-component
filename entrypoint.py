#!/usr/bin/env python3
"""Github action entry point script."""

import glob
import json
import logging
import os
import subprocess
from typing import Dict, List

from pydantic import BaseSettings, Field

logging.basicConfig(level=logging.INFO)


class Config(BaseSettings):  # pylint: disable=R0903
    """Splight CLI configuration parameters."""

    SPLIGHT_ACCESS_ID: str
    SPLIGHT_SECRET_KEY: str
    SPLIGHT_PLATFORM_API_HOST: str = Field(
        "https://api.splight-ai.com",
        env="INPUT_SPLIGHT_PLATFORM_API_HOST",
    )


def configure_cli(config: Dict) -> None:
    """Load configuration to Splight CLI."""
    with subprocess.Popen(
        [
            "/usr/local/bin/splight",
            "configure",
            "--from-json",
            json.dumps(config),
        ],
        stdout=subprocess.DEVNULL,
    ) as p:
        _, error = p.communicate()
        if error:
            raise ChildProcessError(error)
    logging.info("Configuration successful.")


def push_component(path: str) -> None:
    """Push component using Splight CLI."""
    logging.info("Tring to push component at '%s' ...", path)
    cmd = ["/usr/local/bin/splight", "hub", "component", "push", path, "-f"]
    with subprocess.Popen(cmd) as p:
        p.wait()
        if p.returncode != 0:
            logging.error(p.communicate()[0])
            raise ChildProcessError("Error unexpected pushing component.")
    logging.info("Component at %s uploaded successfully.", path)


def find_files(expr: str) -> List:
    """Find files matching the given expression and return
    the parent directory of each one.
    """
    files = glob.glob(expr, recursive=True)
    return files


def main() -> None:
    """Main process."""
    config = Config()
    configure_cli(config.dict())

    files = find_files("./**/spec.json")
    if len(files) == 0:
        raise FileNotFoundError(
            "No 'spec.json' was found inside the repository."
        )
    logging.info("Found these components: %s", files)

    for spec_file in files:
        push_component(os.path.dirname(os.path.abspath(spec_file)))


if __name__ == "__main__":
    main()
