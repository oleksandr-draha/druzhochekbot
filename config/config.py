import base64
from os import path

import msgpack
import yaml
from datetime import datetime


class DruzhochekConfig(object):
    config = None
    errors = []
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

    def log_error(self, error):
        if len(self.errors) >= 100:
            self.errors.pop(0)
        self.errors.append([datetime.now(), error])

    def clean_errors(self):
        self.errors = []

    def repr_errors(self):
        errors = ""
        for date_error, error in self.errors:
            errors += str(date_error) + '\r\n' + error.replace('\n', '\r\n') + '\r\n'
        return errors

    # endregion


config = DruzhochekConfig()
