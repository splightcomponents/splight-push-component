import subprocess
import json
import glob
from os import environ
from os.path import (
    commonpath,
    abspath,
    dirname,
)
from typing import Dict, List
import logging


logging.basicConfig(level=logging.INFO)


def load_secrets() -> Dict:
    
    json_configuration = {
        "SPLIGHT_ACCESS_ID": environ["SPLIGHT_ACCESS_ID"],
        "SPLIGHT_SECRET_KEY": environ["SPLIGHT_SECRET_KEY"],
        "SPLIGHT_PLATFORM_API_HOST": environ["SPLIGHT_PLATFORM_API_HOST"] # TODO esto sacarlo cuando esta en prod. los clientes no van a tener esa var
    }
    return json_configuration

def configure_cli(config: Dict) -> None:
    p = subprocess.Popen(
        ["splight", "configure", "--from-json", json.dumps(config)],
        stdout=subprocess.DEVNULL,
    )
    _, error = p.communicate()
    if error:
        raise Exception(error)
    logging.info("Configuration successful.")

def find_files(expr: str) -> List:
    """Find files matching the given expression and return
    the parent directory of each one.
    """
    files = glob.glob(expr, recursive=True)
    dirs = [dirname(file) for file in files]
    return dirs

def load_wsv(path: str) -> List:
    with open(path, "r") as fp:
        values = fp.readlines()[0].split(" ")
    return values

def modified_roots(roots: List, files: List) -> List:
    """Keep only those roots directories containing at least one of the
    provided files.
    """
    to_update = set()
    for path in roots:
        abs_path = abspath(path)
        for file in files:
            abs_file = abspath(file)
            if commonpath([abs_path]) == commonpath([abspath(abs_path), abspath(abs_file)]):
                to_update.add(path)
    return list(to_update)
    
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
    
    components = find_files("./**/spec.json") 
    if not components:
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

if __name__ == '__main__':
    main()
