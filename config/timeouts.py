from base_config import BaseConfig


class TimeoutsConfig(BaseConfig):
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
