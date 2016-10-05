from os import path

import yaml


class DruzhochekConfig:
    config = None

    def _load_config(self):
        default_config_name = 'config.yaml'
        config_path = path.join(path.dirname(__file__), default_config_name)
        with open(config_path, 'r') as default_config:
            _config = yaml.load(default_config)
        return _config

    def __init__(self):
        self.config = self._load_config()

    @property
    def bot_token(self):
        return self.config.get("bot", {}).get("token")

    @property
    def updates_path(self):
        return self.config.get("bot", {}).get("updates-path")

    @property
    def send_message_path(self):
        return self.config.get("bot", {}).get("send-message-path")

    @property
    def answer_unknown(self):
        return self.config.get("bot", {}).get("answer-unknown")

    @property
    def game_login(self):
        return self.config.get("game", {}).get("login")

    @property
    def game_password(self):
        return self.config.get("game", {}).get("password")

    @property
    def game_host(self):
        return self.config.get("game", {}).get("host")

    @property
    def game_id(self):
        return self.config.get("game", {}).get("id")


config = DruzhochekConfig()
