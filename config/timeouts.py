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
    def codes_interval(self):
        return self.config.get("timeouts", {}).get("codes_interval")

    @codes_interval.setter
    def codes_interval(self, value):
        self.config["timeouts"]["codes_interval"] = value
        self.save_config()

    @property
    def game_update_check_interval(self):
        return self.config.get("timeouts", {}).get("game_update_check_interval")

    @game_update_check_interval.setter
    def game_update_check_interval(self, value):
        self.config["timeouts"]["game_update_check_interval"] = value
        self.save_config()

    @property
    def relogin_interval(self):
        return self.config.get("timeouts", {}).get("relogin_interval")

    @property
    def answer_check_interval(self):
        return self.config.get("timeouts", {}).get("answer_check_interval")
