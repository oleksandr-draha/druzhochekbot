import base64

from base_config import BaseConfig


class GameSettingsConfig(BaseConfig):
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
        self.save_config()

    @property
    def game_login(self):
        login = self.config.get("game", {}).get("login")
        return base64.decodestring(login) if login is not None else None

    @game_login.setter
    def game_login(self, value):
        self.config["game"]["login"] = base64.encodestring(value)
        self.save_config()

    @property
    def game_password(self):
        password = self.config.get("game", {}).get("password")
        return base64.decodestring(password) if password is not None else None

    @game_password.setter
    def game_password(self, value):
        self.config["game"]["password"] = base64.encodestring(value)
        self.save_config()

    @property
    def game_host(self):
        return self.config.get("game", {}).get("host")

    @game_host.setter
    def game_host(self, value):
        self.config["game"]["host"] = value
        self.save_config()

    @property
    def game_id(self):
        return self.config.get("game", {}).get("id")

    @game_id.setter
    def game_id(self, value):
        self.config["game"]["id"] = value
        self.save_config()

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
