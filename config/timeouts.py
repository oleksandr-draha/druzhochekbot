from base_config import BaseConfig


class TimeoutsConfig(BaseConfig):
    @property
    def max_game_attempts(self):
        return self.config.get("timeouts", {}).get("max_attempts")

    @property
    def active_game_interval(self):
        return self.config.get("timeouts", {}).get("active_game_interval")

    @property
    def inactive_game_interval(self):
        return self.config.get("timeouts", {}).get("inactive_game_interval")

    @property
    def process_check_interval(self):
        return self.config.get("timeouts", {}).get("process_check_interval")

    @process_check_interval.setter
    def process_check_interval(self, value):
        self.config["timeouts"]["process_check_interval"] = value
        self.save_config()

    @property
    def relogin_interval(self):
        return self.config.get("timeouts", {}).get("relogin_interval")

    @property
    def answer_check_interval(self):
        return self.config.get("timeouts", {}).get("answer_check_interval")
