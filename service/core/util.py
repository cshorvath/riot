import os
from collections import Mapping
from pathlib import Path
from typing import Tuple

import yaml


class MissingConfigKeyException(Exception):
    def __init__(self, *path) -> None:
        self.path = path
        self.message = "Missing path in configuration file: " + ".".join(path)


class ConfigNode(Mapping):
    def __init__(self, d: dict, *path) -> None:
        self._d = d
        self._path: Tuple = path

    def __getitem__(self, k):
        try:
            item = self._d[k]
            return ConfigNode(item, *self._path, k) if isinstance(item, dict) else item
        except KeyError:
            raise MissingConfigKeyException(*self._path, k)

    def __getattr__(self, item):
        return self[item]

    def __len__(self) -> int:
        return self._d.__len__()

    def __iter__(self):
        return self._d.__iter__()

    def __str__(self):
        return self._d.__str__()

    def __repr__(self):
        return self._d.__repr__()


def parse_config(file_name: str) -> ConfigNode:
    with Path(file_name).open() as f:
        return ConfigNode(yaml.safe_load(f))


def parse_config_from_env(env_var_name: str) -> ConfigNode:
    env_val = os.getenv(env_var_name)
    assert env_val, f"Environment variable {env_var_name} must present"
    return parse_config(env_val)
