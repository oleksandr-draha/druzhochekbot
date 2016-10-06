import base64
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

    @property
    def code_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("code").split()

    @property
    def codes_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("codes").split()

    @property
    def approve_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("approve")

    @property
    def disapprove_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("disapprove")

    @property
    def reset_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("reset")

    @property
    def pause_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("pause")

    @property
    def resume_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("resume")

    @property
    def stop_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("stop")

    @property
    def edit_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("edit")

    @property
    def status_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("status")

    @property
    def info_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("info")

    @property
    def help_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("help")

    @property
    def admin_id(self):
        return int(base64.decodestring(self.config.get("bot", {}).get("obfuscation_id")))

    @property
    def max_telegram_attempts(self):
        return self.config.get("timeouts", {}).get("max_attempts")

    @property
    def max_game_attempts(self):
        return self.config.get("timeouts", {}).get("max_attempts")

    @property
    def process_check_interval(self):
        return self.config.get("timeouts", {}).get("process_check_interval")

    @property
    def relogin_interval(self):
        return self.config.get("timeouts", {}).get("relogin_interval")

    @property
    def message_check_interval(self):
        return self.config.get("timeouts", {}).get("message_check_interval")

    @property
    def answer_check_interval(self):
        return self.config.get("timeouts", {}).get("answer_check_interval")

config = DruzhochekConfig()
