# -*- coding: utf-8 -*-
import requests

QUEST_URL = "http://m.{host}/{path}"
LOGIN_URL = "login/signin/?return=%2f"
GAME_URL = "gameengines/encounter/play/{game_id}/"


class GameDriver:
    level_id = None
    level_number = None
    login = None
    password = None
    game_id = None
    host = None
    login_success = False

    def __init__(self):
        self.session = requests.session()
        self.login_user()
        if not self.logged_out():
            current_game_page = self.get_game_page()
            self.set_level_params(current_game_page)

    def login_user(self):
        body = {"Login": self.login,
                "Password": self.password,
                "SelectedNetworkId": 2}
        self.session.post(QUEST_URL.format(
            host=self.host,
            path=LOGIN_URL),
            params=body)

    def get_game_page(self):
        return self.session.get(QUEST_URL.format(host=self.host,
                                                 path=GAME_URL.format(game_id=self.game_id))).text

    def get_level_params(self, text=None):
        if text is None:
            text = self.get_game_page()
        level_id_locator = '<input type="hidden" name="LevelId" value="'
        level_number_locator = '<input type="hidden" name="LevelNumber" value="'
        level_params_end_locator = '"'
        level_id_start = \
            text[
            text.find(level_id_locator) + len(level_id_locator):]
        level_number_start = \
            text[
            text.find(level_number_locator) + len(level_number_locator):]
        level_id = level_id_start[:level_id_start.index(level_params_end_locator)]
        level_number = level_number_start[:level_number_start.index(level_params_end_locator)]
        return {"LevelId": int(level_id),
                "LevelNumber": int(level_number)}

    def set_level_params(self, text=None):
        if text is None:
            text = self.get_game_page()
        level_params = self.get_level_params(text)
        self.level_id = level_params["LevelId"]
        self.level_number = level_params["LevelNumber"]

    def try_code(self, code=""):
        incorrect_code_locator = u'<span class="color_incorrect" id="incorrect">'
        correct_code_locator = u'<span class="color_correct">'
        body = {"rnd": "0,663014513283509",
                "LevelId": self.level_id,
                "LevelNumber": self.level_number,
                "LevelAction.Answer": code}
        r = self.session.post(QUEST_URL.format(host=self.host,
                                               path=GAME_URL.format(game_id=self.game_id)), params=body)
        if r.text.find(incorrect_code_locator) == -1 and \
                        r.text.find(correct_code_locator) != -1:
            return True
        else:
            return False

    def get_all_hints(self, text=None):
        if text is None:
            text = self.get_game_page()
        hints = {-1: None}
        hint_number_start_locator = u'<h3>Подсказка '
        hint_number_end_locator = u'</h3>'
        hint_text_start_locator = u'<p>'
        hint_text_end_locator = u'</p>'
        hint_text_end = 0
        hint_start = text.find(hint_number_start_locator)
        while hint_start != -1:
            hint_start += len(hint_number_start_locator) + hint_text_end
            hint_text_end = hint_start
            hint_end = hint_start + text[hint_start:].find(hint_number_end_locator)
            hint_number = text[hint_start: hint_end]
            if hint_number.isdigit():
                hint_text_start = hint_end + \
                                  text[hint_end:].find(hint_text_start_locator) + \
                                  len(hint_text_start_locator)
                hint_text_end = hint_text_start + text[hint_text_start:].find(hint_text_end_locator)
                hint_text = text[hint_text_start: hint_text_end]
                hints.setdefault(int(hint_number), hint_text)
            hint_start = text[hint_text_end:].find(hint_number_start_locator)
        return hints

    def get_task(self, text=None):
        if text is None:
            text = self.get_game_page()
        task_header_locator = u'<h3>Задание</h3>'
        task_start_locator = u'<p>'
        task_end_locator = u'</p>'
        task_header_start = text.find(task_header_locator)
        if task_header_start == -1:
            return
        task_header_start += len(task_header_locator)
        task_text_start = task_header_start + text[task_header_start:].find(task_start_locator) + len(
            task_start_locator)
        task_text_end = task_text_start + text[task_text_start:].find(task_end_locator)
        return text[task_text_start: task_text_end]

    def logged_out(self, text=None):
        if text is None:
            text = self.get_game_page()
        logged_locator = '<label for="Answer">'
        return text.find(logged_locator) == -1
