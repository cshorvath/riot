import os
from pathlib import Path

import yaml


def parse_config(file_name: str):
    with Path(file_name).open() as f:
        return yaml.safe_load(f)


def parse_config_from_env(env_var_name: str) -> dict:
    env_val = os.getenv(env_var_name)
    assert env_val, f"Environment variable {env_var_name} must present"
    return parse_config(env_val)
