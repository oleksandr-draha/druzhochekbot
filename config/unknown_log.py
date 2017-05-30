from datetime import datetime

from base_config import BaseConfig


class UnknownLog(BaseConfig):
    @property
    def unknown_raw(self):
        return self.config.get("unknown", [])

    @unknown_raw.setter
    def unknown_raw(self, value):
        self.config["unknown"] = value
        self.save_config()

    def log_unknown(self, message):
        unknowns = self.unknown_raw
        if len(unknowns) >= 100:
            unknowns.pop(0)
        unknowns.append({"timestamp": datetime.now(),
                         "user_id": message["from_id"],
                         "username": message["username"],
                         "message_text": message["text"]})
        self.unknown_raw = unknowns

    def clean_unknown(self):
        self.unknown_raw = []

    def repr_unknown(self):
        unknown_message = ""
        for unknown in self.unknown_raw:
            unknown_message += u"{timestamp}\r\n{user_id} : {username}\r\n{message}\r\n\r\n".format(
                timestamp=unknown["timestamp"],
                user_id=unknown["user_id"],
                message=unknown["message_text"],
                username=unknown["username"])
        return unknown_message
