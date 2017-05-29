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

    # region Game settings

    @property
    def quest_images_url(self):
        return self.config.get("game", {}).get("quest_images_url")

    @property
    def quest_game_url(self):
        return self.config.get("game", {}).get("quest_game_url")

    @property
    def quest_login_url(self):
        return self.config.get("game", {}).get("quest_login_url")

    @property
    def quest_url(self):
        return self.config.get("game", {}).get("quest_url")

    @property
    def code_limit(self):
        return self.config.get("game", {}).get("code_limit")

    @code_limit.setter
    def code_limit(self, value):
        self.config["game"]["code_limit"] = value
        if self.autosave:
            config.save_config()

    @property
    def game_login(self):
        login = self.config.get("game", {}).get("login")
        return base64.decodestring(login) if login is not None else None

    @game_login.setter
    def game_login(self, value):
        self.config["game"]["login"] = base64.encodestring(value)
        if self.autosave:
            config.save_config()

    @property
    def game_password(self):
        password = self.config.get("game", {}).get("password")
        return base64.decodestring(password) if password is not None else None

    @game_password.setter
    def game_password(self, value):
        self.config["game"]["password"] = base64.encodestring(value)
        if self.autosave:
            config.save_config()

    @property
    def game_host(self):
        return self.config.get("game", {}).get("host")

    @game_host.setter
    def game_host(self, value):
        self.config["game"]["host"] = value
        if self.autosave:
            config.save_config()

    @property
    def game_id(self):
        return self.config.get("game", {}).get("id")

    @game_id.setter
    def game_id(self, value):
        self.config["game"]["id"] = value
        if self.autosave:
            config.save_config()

    @property
    def show_codes_left(self):
        return [int(i) for i in self.config.get("game", {}).get("show_codes_left").split()]

    @property
    def show_time_to_hint(self):
        return self.config.get("game", {}).get("show_time_to_hint")

    @property
    def show_time_left_minutes(self):
        return self.config.get("game", {}).get("show_time_left_minutes").split()

    @property
    def show_first_ap_time(self):
        return self.config.get("game", {}).get("show_first_ap_time")

    @property
    def show_first_hint_time(self):
        return self.config.get("game", {}).get("show_first_hint_time")

    # endregion


    # region Timeouts

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

    # endregion


config = DruzhochekConfig()
