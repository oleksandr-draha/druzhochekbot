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

    def __init__(self):
        self.config = self._load_config()

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

    def log_error(self, error):
        if len(self.errors) >= 100:
            self.errors.pop(0)
        self.errors.append([datetime.now(), error])

    def repr_errors(self):
        errors = ""
        for date_error, error in self.errors:
            errors += str(date_error) + '\r\n' + error.replace('\n', '\r\n') + '\r\n'
        return errors

    # endregion

    # region Bot settings section

    @property
    def bot_token(self):
        return self.config.get("bot", {}).get("token")

    @bot_token.setter
    def bot_token(self, value):
        self.config["bot"]["token"] = value
        if self.autosave:
            config.save_config()

    @property
    def group_chat_id(self):
        return self.config.get("bot", {}).get("approved_chat")

    @group_chat_id.setter
    def group_chat_id(self, value):
        self.config["bot"]["approved_chat"] = value
        if self.autosave:
            config.save_config()

    @property
    def paused(self):
        return self.config.get("bot", {}).get("paused")

    @paused.setter
    def paused(self, value):
        self.config["bot"]["paused"] = value
        if self.autosave:
            config.save_config()

    @property
    def autosave(self):
        return self.config.get("bot", {}).get("autosave")

    @autosave.setter
    def autosave(self, value):
        self.config["bot"]["autosave"] = value
        if self.autosave:
            config.save_config()

    @property
    def updates_path(self):
        return self.config.get("bot", {}).get("updates-path")

    @property
    def users_path(self):
        return self.config.get("bot", {}).get("users-path")

    @property
    def send_document_path(self):
        return self.config.get("bot", {}).get("send-document-path")

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
    def passphrases(self):
        return [self.admin_passphrase, self.field_passphrase, self.kc_passphrase]

    @property
    def admin_passphrase(self):
        raw = self.config.get("bot", {}).get("admin_passphrase")
        return base64.decodestring(raw)

    @property
    def field_passphrase(self):
        raw = self.config.get("bot", {}).get("field_passphrase")
        return base64.decodestring(raw)

    @property
    def kc_passphrase(self):
        raw = self.config.get("bot", {}).get("kc_passphrase")
        return base64.decodestring(raw)

    @admin_passphrase.setter
    def admin_passphrase(self, passphrase):
        self.config["bot"]["admin_passphrase"] = base64.encodestring(passphrase)
        if self.autosave:
            config.save_config()

    @field_passphrase.setter
    def field_passphrase(self, passphrase):
        self.config["bot"]["field_passphrase"] = base64.encodestring(passphrase)
        if self.autosave:
            config.save_config()

    @kc_passphrase.setter
    def kc_passphrase(self, passphrase):
        self.config["bot"]["kc_passphrase"] = base64.encodestring(passphrase)
        if self.autosave:
            config.save_config()

    @property
    def admin_ids(self):
        raw = self.config.get("bot", {}).get("obfuscation_id")
        if raw is None:
            return []
        decoded = base64.decodestring(raw)
        admins = msgpack.loads(decoded)
        return admins

    @admin_ids.setter
    def admin_ids(self, ids):
        self.config["bot"]["obfuscation_id"] = ids
        if self.autosave:
            config.save_config()

    def add_admin_id(self, admin_id):
        admin_ids = self.admin_ids + [admin_id]
        encoded = msgpack.dumps(admin_ids)
        self.admin_ids = base64.encodestring(encoded)
        if self.autosave:
            config.save_config()

    def delete_admin_id(self, admin_id):
        admin_ids = self.admin_ids[:]
        admin_ids.remove(admin_id)
        encoded = msgpack.dumps(admin_ids)
        self.admin_ids = base64.encodestring(encoded)
        if self.autosave:
            config.save_config()

    def clear_admins(self):
        encoded = msgpack.dumps([])
        self.admin_ids = base64.encodestring(encoded)
        if self.autosave:
            config.save_config()

    def clear_fields(self):
        encoded = msgpack.dumps([])
        self.field_ids = base64.encodestring(encoded)
        if self.autosave:
            config.save_config()

    def clear_kcs(self):
        encoded = msgpack.dumps([])
        self.kc_ids = base64.encodestring(encoded)
        if self.autosave:
            config.save_config()

    @property
    def field_ids(self):
        raw = self.config.get("bot", {}).get("field_ids")
        if raw is None:
            return []
        decoded = base64.decodestring(raw)
        fields = msgpack.loads(decoded)
        return fields

    @field_ids.setter
    def field_ids(self, ids):
        self.config["bot"]["field_ids"] = ids
        if self.autosave:
            config.save_config()

    def add_field_id(self, field_id):
        field_ids = self.field_ids + [field_id]
        encoded = msgpack.dumps(field_ids)
        self.field_ids = base64.encodestring(encoded)
        if self.autosave:
            config.save_config()

    def delete_field_id(self, field_id):
        field_ids = self.field_ids[:]
        field_ids.remove(field_id)
        encoded = msgpack.dumps(field_ids)
        self.field_ids = base64.encodestring(encoded)
        if self.autosave:
            config.save_config()

    @property
    def kc_ids(self):
        raw = self.config.get("bot", {}).get("kc_ids")
        if raw is None:
            return []
        decoded = base64.decodestring(raw)
        kcs = msgpack.loads(decoded)
        return kcs

    @kc_ids.setter
    def kc_ids(self, ids):
        self.config["bot"]["kc_ids"] = ids
        if self.autosave:
            config.save_config()

    def add_kc_id(self, kc_id):
        kc_ids = self.kc_ids + [kc_id]
        encoded = msgpack.dumps(kc_ids)
        self.kc_ids = base64.encodestring(encoded)
        if self.autosave:
            config.save_config()

    def delete_kc_id(self, kc_id):
        kc_ids = self.kc_ids[:]
        kc_ids.remove(kc_id)
        encoded = msgpack.dumps(kc_ids)
        self.kc_ids = base64.encodestring(encoded)
        if self.autosave:
            config.save_config()

    @staticmethod
    def is_user(from_id):
        return from_id in config.admin_ids + config.field_ids + config.field_ids

    @staticmethod
    def is_admin(from_id):
        return from_id in config.admin_ids

    @staticmethod
    def is_field(from_id):
        return from_id in config.field_ids

    @staticmethod
    def is_kc(from_id):
        return from_id in config.kc_ids

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

    # region Commands section

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
    def codes_history_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("codes_history")

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
    def delete_field_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("delete_field")

    @property
    def delete_kc_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("delete_kc")

    @property
    def edit_admin_pass(self):
        return self.config.get("bot", {}).get("commands", {}).get("edit_admin_pass")

    @property
    def edit_field_pass(self):
        return self.config.get("bot", {}).get("commands", {}).get("edit_field_pass")

    @property
    def edit_kc_pass(self):
        return self.config.get("bot", {}).get("commands", {}).get("edit_kc_pass")

    @property
    def clearadmin_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("clearadmin")

    @property
    def clearfield_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("clearfield")

    @property
    def clearkc_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("clearkc")

    @property
    def alert_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("alert")

    @property
    def chat_message_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("chat_message")

    @property
    def token_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("token")

    @property
    def message_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("message")

    @property
    def message_admin_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("message_admin")

    @property
    def message_field_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("message_field")

    @property
    def message_kc_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("message_kc")

    @property
    def send_source_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("send_source")

    @property
    def send_errors_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("errors")

    @property
    def send_unknown_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("unknown")

    @property
    def codes_limit_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("codes_limit")

    @property
    def login_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("login")

    @property
    def pass_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("pass")

    @property
    def host_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("host")

    @property
    def game_command(self):
        return self.config.get("bot", {}).get("commands", {}).get("game")

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
