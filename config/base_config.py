from os import path

import yaml
from datetime import datetime


class BaseConfig(object):
    start_time = datetime.now()

    # region System

    def __init__(self, path="config.yaml"):
        self.path = path
        self.config = self._load_config()

    def _load_config(self):
        config_path = path.join(path.dirname(__file__), self.path)
        with open(config_path, 'r') as default_config:
            _config = yaml.load(default_config)
        return _config

    def save_config(self):
        config_path = path.join(path.dirname(__file__), self.path)
        try:
            with open(config_path, 'w') as default_config:
                yaml.dump(self.config, default_config)
            return True
        except IOError:
            return False
