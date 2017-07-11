import base64

import msgpack

from base_config import BaseConfig


class BotSettingsConfig(BaseConfig):

    @property
    def bot_token(self):
        return self.config.get("bot", {}).get("token")

    @bot_token.setter
    def bot_token(self, value):
        self.config["bot"]["token"] = value
        self.save_config()

    @property
    def group_chat_id(self):
        return self.config.get("bot", {}).get("approved_chat")

    @group_chat_id.setter
    def group_chat_id(self, value):
        self.config["bot"]["approved_chat"] = value
        self.save_config()

    @property
    def paused(self):
        return self.config.get("bot", {}).get("paused")

    @paused.setter
    def paused(self, value):
        self.config["bot"]["paused"] = value
        self.save_config()

    @property
    def connection_problems(self):
        return self.config.get("bot", {}).get("connection_problems")

    @connection_problems.setter
    def connection_problems(self, value):
        self.config["bot"]["connection_problems"] = value
        self.save_config()

    @property
    def tag_field(self):
        return self.config.get("bot", {}).get("tag_field")

    @tag_field.setter
    def tag_field(self, value):
        self.config["bot"]["tag_field"] = value
        self.save_config()

    @property
    def log_activity(self):
        return self.config.get("bot", {}).get("log_activity")

    @log_activity.setter
    def log_activity(self, value):
        self.config["bot"]["log_activity"] = value
        self.save_config()

    @property
    def autohandbrake(self):
        return self.config.get("bot", {}).get("autohandbrake")

    @autohandbrake.setter
    def autohandbrake(self, value):
        self.config["bot"]["autohandbrake"] = value
        self.save_config()

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
        self.save_config()

    @field_passphrase.setter
    def field_passphrase(self, passphrase):
        self.config["bot"]["field_passphrase"] = base64.encodestring(passphrase)
        self.save_config()

    @kc_passphrase.setter
    def kc_passphrase(self, passphrase):
        self.config["bot"]["kc_passphrase"] = base64.encodestring(passphrase)
        self.save_config()

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
        self.save_config()

    def add_admin_id(self, admin_id):
        admin_ids = self.admin_ids + [admin_id]
        encoded = msgpack.dumps(admin_ids)
        self.admin_ids = base64.encodestring(encoded)
        self.save_config()

    def delete_admin_id(self, admin_id):
        admin_ids = self.admin_ids[:]
        admin_ids.remove(admin_id)
        encoded = msgpack.dumps(admin_ids)
        self.admin_ids = base64.encodestring(encoded)
        self.save_config()

    def clean_admins(self):
        encoded = msgpack.dumps([])
        self.admin_ids = base64.encodestring(encoded)
        self.save_config()

    def clean_fields(self):
        encoded = msgpack.dumps([])
        self.field_ids = base64.encodestring(encoded)
        self.save_config()

    def clean_kcs(self):
        encoded = msgpack.dumps([])
        self.kc_ids = base64.encodestring(encoded)
        self.save_config()

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
        self.save_config()

    def add_field_id(self, field_id):
        field_ids = self.field_ids + [field_id]
        encoded = msgpack.dumps(field_ids)
        self.field_ids = base64.encodestring(encoded)
        self.save_config()

    def delete_field_id(self, field_id):
        field_ids = self.field_ids[:]
        field_ids.remove(field_id)
        encoded = msgpack.dumps(field_ids)
        self.field_ids = base64.encodestring(encoded)
        self.save_config()

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
        self.save_config()

    def add_kc_id(self, kc_id):
        kc_ids = self.kc_ids + [kc_id]
        encoded = msgpack.dumps(kc_ids)
        self.kc_ids = base64.encodestring(encoded)
        self.save_config()

    def delete_kc_id(self, kc_id):
        kc_ids = self.kc_ids[:]
        kc_ids.remove(kc_id)
        encoded = msgpack.dumps(kc_ids)
        self.kc_ids = base64.encodestring(encoded)
        self.save_config()

    def is_user(self, from_id):
        return from_id in self.admin_ids + self.field_ids + self.kc_ids

    def is_admin(self, from_id):
        return from_id in self.admin_ids

    def is_field(self, from_id):
        return from_id in self.field_ids

    def is_kc(self, from_id):
        return from_id in self.kc_ids
