#!/usr/bin/env python3

import json
import os
import logging
import subprocess
from typing import Dict, List

logging.basicConfig(level=logging.INFO)


def load_secrets() -> Dict:
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

def push_component(components: List):
    for path in components:
        print(f"Starting with {path}...")
        cmd = ["splight", "hub", "component", "push", f"{path}", "-f"]
        p = subprocess.Popen(cmd)
        p.wait()
        if p.returncode != 0:
            raise Exception("Error unexpected pushing component.")
        logging.info(f"Component at {path} uploaded successfully.")

def main() -> None:
    config = load_secrets()
    configure_cli(config)
    
    if not os.path.isfile(os.environ["INPUT_SPEC_FILE"]):
        raise Exception("No 'spec.json' was found inside the repository.")
    logging.info(f"Found these components: {components}.")

    changed_files = load_wsv(".github/outputs/all_changed_and_modified_files.txt")
    logging.info(f"Changed files are: {changed_files}")
    
    to_update = modified_roots(components, changed_files)
    if not to_update:
        logging.warning("No component was modified.")
        return
    print(f"The following components will be updated: {list(to_update)}.")
    
    push_component(to_update)
    logging.info("Done.")

if __name__ == "__main__":
    main()
