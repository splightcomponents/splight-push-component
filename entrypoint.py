#!/usr/bin/env python3

import json
import os
import logging
import subprocess
from typing import Dict, List

logging.basicConfig(level=logging.INFO)


def load_config() -> Dict:
    config = {
        "SPLIGHT_ACCESS_ID": os.environ["INPUT_SPLIGHT_ACCESS_ID"],
        "SPLIGHT_SECRET_KEY": os.environ["INPUT_SPLIGHT_SECRET_KEY"],
    }

    if os.environ["INPUT_SPLIGHT_PLATFORM_API_HOST"]:
        config["SPLIGHT_PLATFORM_API_HOST"] = os.environ["INPUT_SPLIGHT_PLATFORM_API_HOST"]
    return config

def configure_cli(config: Dict) -> None:
    p = subprocess.Popen(
        ["splight", "configure", "--from-json", json.dumps(config)],
        stdout=subprocess.DEVNULL,
    )
    _, error = p.communicate()
    if error:
        raise Exception(error)
    logging.info("Configuration successful.")

def push_component(path: str) -> None:
    print(f"Tring to push component at {path}...")
    cmd = ["splight", "hub", "component", "push", f"{path}", "-f"]
    p = subprocess.Popen(cmd)
    p.wait()
    if p.returncode != 0:
        logging.error(p.communicate()[0])
        raise Exception("Error unexpected pushing component.")
    logging.info(f"Component at {path} uploaded successfully.")

def main() -> None:
    config = load_config()
    configure_cli(config)
    
    spec_file = os.environ["INPUT_SPEC_FILE"]
    if not os.path.isfile(spec_file):
        raise FileNotFoundError("No 'spec.json' was found inside the repository.")

    push_component(os.path.dirname(spec_file))

if __name__ == "__main__":
    main()
