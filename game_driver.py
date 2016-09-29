import requests

user_name = "druzhochek"
password = ""

QUEST_URL = "http://m.online.quest.ua/{path}"
LOGIN_URL = "login/signin/?return=%2f"
GAME_ID = 36855
GAME_URL = "gameengines/encounter/play/{game_id}/".format(game_id=GAME_ID)


class GameDriver():
    stoken = None
    session = None
    level_id = None
    level_number = None

    def __init__(self):
        self.session = requests.session()
        self.login_user()
        self.get_level_params()

    def login_user(self):
        body = {"Login": user_name,
                "Password": password,
                "SelectedNetworkId": 2}
        r = self.session.post(QUEST_URL.format(path=LOGIN_URL), params=body)
        cookies = r.headers['Set-cookie']
        stoken_with_more = cookies[cookies.index("stoken") + len("stoken") + 1:]
        self.stoken = stoken_with_more[:stoken_with_more.index(';')]
        return self.stoken

    def get_level_params(self):
        level_id_locator = '<input type="hidden" name="LevelId" value="'
        level_number_locator = '<input type="hidden" name="LevelNumber" value="'
        r = self.session.get(QUEST_URL.format(path=GAME_URL))
        level_id_start = \
            r.content[
            r.content.index(level_id_locator) + len(level_id_locator):]
        level_number_start = \
            r.content[
            r.content.index(level_number_locator) + len(level_number_locator):]
        self.level_id = level_id_start[:level_id_start.index('"')]
        self.level_number = level_number_start[:level_number_start.index('"')]
        return {"LevelId": self.level_id,
                "LevelNumber": self.level_number}

    def try_code(self, code=""):
        body = {"rnd": "0,663014513283509",
            "LevelId": self.level_id,
            "LevelNumber": self.level_number,
            "LevelAction.Answer": code}
        r = self.session.post(QUEST_URL.format(path=LOGIN_URL), params=body)
        pass

game = GameDriver()
game.get_level_params()
game.try_code("ddddd")
