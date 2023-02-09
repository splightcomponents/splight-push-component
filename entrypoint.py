#!/usr/bin/env python3
"""Github action entry point script."""

import json
import logging
import os
import subprocess
from typing import Dict

logging.basicConfig(level=logging.INFO)


def load_config() -> Dict:
    """Load secrets from action input arguments."""
    config = {
        "SPLIGHT_ACCESS_ID": os.environ["INPUT_SPLIGHT_ACCESS_ID"],
        "SPLIGHT_SECRET_KEY": os.environ["INPUT_SPLIGHT_SECRET_KEY"],
    }
    logging.info(config)
    if os.environ["INPUT_SPLIGHT_PLATFORM_API_HOST"]:
        config["SPLIGHT_PLATFORM_API_HOST"] = os.environ["INPUT_SPLIGHT_PLATFORM_API_HOST"]
    return config


def configure_cli(config: Dict) -> None:
    """Load configuration to Splight CLI."""
    with subprocess.Popen(
        ["/usr/local/bin/splight", "configure", "--from-json", json.dumps(config)],
        stdout=subprocess.DEVNULL,
    ) as p:
        _, error = p.communicate()
        if error:
            raise ChildProcessError(error)
    logging.info("Configuration successful.")


def push_component(path: str) -> None:
    """Push component using Splight CLI."""
    logging.info("Tring to push component at %s...", path)
    cmd = ["/usr/local/bin/splight", "hub", "component", "push", path, "-f"]
    with subprocess.Popen(cmd) as p:
        p.wait()
        if p.returncode != 0:
            logging.error(p.communicate()[0])
            raise ChildProcessError("Error unexpected pushing component.")
    logging.info("Component at %s uploaded successfully.", path)


def main() -> None:
    """Main process."""
    config = load_config()
    configure_cli(config)

    spec_file = os.environ["INPUT_SPEC_FILE"]
    if not os.path.isfile(spec_file):
        raise FileNotFoundError("No 'spec.json' was found inside the repository.")

    push_component(os.path.dirname(os.path.abspath(spec_file)))


if __name__ == "__main__":
    main()
