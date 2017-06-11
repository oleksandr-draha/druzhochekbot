from datetime import datetime

from base_config import BaseConfig


class ActivityLog(BaseConfig):

    @property
    def activity(self):
        return self.config.get("activity")

    @activity.setter
    def activity(self, value):
        self.config["activity"] = value
        self.save_config()

    def log_activity(self):
        self.activity = datetime.now()
