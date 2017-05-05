import base64
from os import path

import yaml


class DruzhochekConfig(object):
    config = None

    def _load_config(self):
        default_config_name = 'config.yaml'
        config_path = path.join(path.dirname(__file__), default_config_name)
        with open(config_path, 'r') as default_config:
            _config = yaml.load(default_config)
        return _config

    def save_config(self):
        default_config_name = 'config.yaml'
        config_path = path.join(path.dirname(__file__), default_config_name)
        try:
            with open(config_path, 'w') as default_config:
                yaml.dump(self.config, default_config)
            return True
        except IOError:
            return False

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
    def answer_forbidden(self):
        return self.config.get("bot", {}).get("answer-forbidden")

    @property
    def game_login(self):
        login = self.config.get("game", {}).get("login")
        return base64.decodestring(login) if login is not None else None

    @game_login.setter
    def game_login(self, value):
        self.config["game"]["login"] = base64.encodestring(value)

    @property
    def game_password(self):
        password = self.config.get("game", {}).get("password")
        return base64.decodestring(password) if password is not None else None

    @game_password.setter
    def game_password(self, value):
        self.config["game"]["password"] = base64.encodestring(value)

    @property
    def game_host(self):
        return self.config.get("game", {}).get("host")

    @game_host.setter
    def game_host(self, value):
        self.config["game"]["host"] = value

    @property
    def game_id(self):
        return self.config.get("game", {}).get("id")

    @game_id.setter
    def game_id(self, value):
        self.config["game"]["id"] = value

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
    def save_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("save")

    @property
    def status_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("status")

    @property
    def task_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("task")

    @property
    def hints_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("hints")

    @property
    def info_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("info")

    @property
    def help_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("help")

    @property
    def gap_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("gap")

    @property
    def cancel_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("cancel")

    @property
    def add_admin_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("add_admin")

    @property
    def delete_admin_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("delete_admin")

    @property
    def add_field_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("add_field")

    @property
    def add_kc_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("add_kc")

    @property
    def admin_ids(self):
        decoded = self.config.get("bot", {}).get("obfuscation_id").split()
        return [int(base64.decodestring(admin_id)) for admin_id in decoded]

    @admin_ids.setter
    def admin_ids(self, ids):
        self.config["bot"]["obfuscation_id"] = ','.join(ids)

    def add_admin_id(self, admin_id):
        admin_ids = self.admin_ids + [admin_id]
        encoded = [base64.encodestring(str(a)) for a in admin_ids]
        self.admin_ids = encoded

    def delete_admin_id(self, admin_id):
        admin_ids = self.admin_ids[:]
        admin_ids.remove(admin_id)
        encoded = [base64.encodestring(str(a)) for a in admin_ids]
        self.admin_ids = encoded

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


config = DruzhochekConfig()
