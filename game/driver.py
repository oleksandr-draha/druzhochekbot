# -*- coding: utf-8 -*-
import re

from requests import ConnectionError, session
import html2text

QUEST_URL = "http://m.{host}/{path}"
LOGIN_URL = "login/signin/?return=%2f"
GAME_URL = "gameengines/encounter/play/{game_id}/"
IMAGES_URL = "http://d1.endata.cx/data/games/{game_id}{image_name}"


class GameDriver:
    level_id = None
    level_number = None
    login = None
    password = None
    game_id = None
    host = None
    connected = False

    def __init__(self):
        self.session = session()
        try:
            self.login_user()
            game_page = self.get_game_page()
            if self.is_logged(game_page) and not self.is_finished(game_page):
                self.set_level_params(game_page)
            self.connected = True
        except ConnectionError:
            self.connected = False

    def login_user(self):
        try:
            body = {"Login": self.login,
                    "Password": self.password,
                    "SelectedNetworkId": 2}
            return self.session.post(QUEST_URL.format(
                host=self.host,
                path=LOGIN_URL),
                params=body).text
        except ConnectionError:
            return ''

    def is_logged(self, text=None):
        if text is None:
            text = self.get_game_page()
        logged_locator = '<label for="Answer">'
        finish_locator = u'<font size="+2"><span id="animate">Поздравляем!!!</span></font>'
        return text.find(logged_locator) != -1 or text.find(finish_locator) != -1

    def is_finished(self, text=None):
        if text is None:
            text = self.get_game_page()
        finish_locator = u'<font size="+2"><span id="animate">Поздравляем!!!</span></font>'
        return text.find(finish_locator) != -1

    def get_game_page(self):
        try:
            return self.session.get(
                QUEST_URL.format(host=self.host,
                                 path=GAME_URL.format(game_id=self.game_id))).text
        except ConnectionError:
            return ""

    def post_game_page(self, body):
        try:
            return self.session.post(
                QUEST_URL.format(host=self.host,
                                 path=GAME_URL.format(game_id=self.game_id)), params=body)
        except ConnectionError:
            return ""

    # TODO: to parsers
    def get_level_params(self, text=None):
        if text is None:
            text = self.get_game_page()
        level_id_locator = '<input type="hidden" name="LevelId" value="'
        level_number_locator = '<input type="hidden" name="LevelNumber" value="'
        level_params_end_locator = '"'
        level_id_start = \
            text[text.find(level_id_locator) +
                 len(level_id_locator):]
        level_number_start = \
            text[text.find(level_number_locator) +
                 len(level_number_locator):]
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
        r = self.post_game_page(body=body)
        if r.text.find(incorrect_code_locator) == -1 \
                and r.text.find(correct_code_locator) != -1:
            return True
        else:
            return False

    def get_all_hints(self, text=None):

        # TODO: To parsers
        # TODO: Add hints with penalties!
        # <h3 class="inline">Штрафная подсказка
        # <div class="spacer"></div>
        # <h3 class="inline">Штрафная подсказка 1</h3>
        # <p>абриколь</p>
        if text is None:
            text = self.get_game_page()
        hints = {}
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
                hint_text_start = \
                    hint_end + \
                    text[hint_end:].find(hint_text_start_locator) + \
                    len(hint_text_start_locator)
                hint_text_end = hint_text_start + text[hint_text_start:].find(hint_text_end_locator)
                hint_text = text[hint_text_start: hint_text_end]
                hint_text = html2text.html2text(hint_text)
                hints.setdefault(int(hint_number), hint_text)
            hint_start = text[hint_text_end:].find(hint_number_start_locator)
        return hints

    # TODO: To parsers
    def get_task(self, text=None):
        if text is None:
            text = self.get_game_page()
        task_header_locator = u'<h3>Задание</h3>'
        another_task_header_locator = u'<h2>Уровень <span>'
        task_start_locator = u'<p>'
        task_end_locator = u'</p>'
        task_header_start = text.find(task_header_locator)
        if task_header_start == -1 and text.find(another_task_header_locator)==-1:
            return
        task_header_start += len(task_header_locator)
        task_text_start = \
            task_header_start + \
            text[task_header_start:].find(task_start_locator) + \
            len(task_start_locator)
        task_text_end = \
            task_text_start + \
            text[task_text_start:].find(task_end_locator)
        # task_text = self.replace_image_texts(text[task_text_start: task_text_end])
        task_text = html2text.html2text(text[task_text_start: task_text_end])
        return task_text

    def get_ap_text(self, text=None):
        if text is None:
            text = self.get_game_page()
        ap_locator = '<h3 class="timer">'
        ap_end_locator = '</h3>'
        ap_start = text.find(ap_locator)
        if ap_start != -1:
            ap_start += len(ap_locator)
            ap_end = ap_start + text[ap_start:].find(ap_end_locator)
            return html2text.html2text(text[ap_start: ap_end])

    def get_codes_left_text(self, text=None):
        if text is None:
            text = self.get_game_page()
        codes_left_locator = u'осталось закрыть'
        codes_left_end_locator = u')</span>'
        codes_left_start = text.find(codes_left_locator)
        if codes_left_start != -1:
            codes_left_start += len(codes_left_locator)
            codes_left_end = codes_left_start + text[codes_left_start:].find(codes_left_end_locator)
            return int(html2text.html2text(text[codes_left_start: codes_left_end]))

    def get_finish_message(self, text):
        if text is None:
            text = self.get_game_page()
        finish_start_locator = u'<div class="t_center">'
        finish_end_locator = u'</div>'
        finish_start = text.find(finish_start_locator)
        if finish_start != -1:
            finish_start += len(finish_start_locator)
            finish_end = finish_start + text[finish_start:].find(finish_end_locator)
            return html2text.html2text(text[finish_start: finish_end])
