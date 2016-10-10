# -*- coding: utf-8 -*-
from time import sleep

from config.config import config
from config.dictionary import NEW_TASK_MESSAGE, NEW_HINT_MESSAGE, TASK_EDITED_MESSAGE, CODES_LEFT_TEXT
from game.driver import GameDriver

REPLACE_DICTIONARY = {u'<br/>': "\r\n",
                      u'**Автопереход**': u'<b>Автопереход</b>'}


class GameWorker:
    last_level_shown = None
    last_task_text = None
    ap_time_shown = []
    codes_left_shown = []
    hints_shown = []
    connected = False
    finished_shown = False
    codes_limit_shown = False

    def __init__(self):
        self.game_driver = GameDriver()
        self.connected = self.game_driver.connected

    @staticmethod
    def replace_forbidden_words(updates):
        """
        :param updates:
        :type updates: list of str
        :return:
        """
        replaced_updates = []
        for update in updates:
            for word, replace in REPLACE_DICTIONARY.iteritems():
                update = update.replace(word, replace)
            replaced_updates.append(update)
        return replaced_updates

    def reset(self):
        self.last_level_shown = None
        self.last_task_text = None
        self.ap_time_shown = []
        self.codes_left_shown = []
        self.hints_shown = []
        self.finished_shown = False
        self.codes_limit_shown = False

    def check_updates(self):
        updates = []
        game_page = self.game_driver.get_game_page()
        attempt = 0
        while not self.game_driver.is_logged(game_page) and attempt < config.max_game_attempts:
            game_page = self.game_driver.login_user()
            attempt += 1
            sleep(config.relogin_interval)
        if attempt >= config.max_game_attempts:
            return
        if self.game_driver.is_finished(game_page):
            # If game is finished - updates should not be checked
            if not self.finished_shown:
                self.finished_shown = True
                updates.append(self.game_driver.get_finish_message(game_page))
            return updates
        task_text = self.game_driver.get_task(game_page)
        if task_text is None:
            return
        current_level = self.game_driver.get_level_params(game_page)
        self.game_driver.set_level_params(game_page)
        hints = self.game_driver.get_all_hints(game_page)
        # If new task was received:
        if self.last_level_shown != current_level["LevelNumber"] or self.last_level_shown is None:
            self.last_level_shown = current_level["LevelNumber"]
            self.hints_shown = []
            self.ap_time_shown = []
            self.codes_left_shown = []
            self.last_task_text = task_text
            updates.append(NEW_TASK_MESSAGE.format(
                level_number=current_level["LevelNumber"],
                task=task_text))
        # Process AP time
        ap_text = self.game_driver.get_ap_text(game_page)
        if ap_text is not None:
            if config.show_first_ap_time and "first" not in self.ap_time_shown:
                updates.append(ap_text)
                self.ap_time_shown.append("first")
            for ap_time in config.show_ap_for_time:
                minute_locator = u" {minutes} минут".format(minutes=ap_time)
                hour = u"час "
                if minute_locator in ap_text and ap_time not in self.ap_time_shown\
                        and hour not in ap_text:
                    updates.append(ap_text)
                    self.ap_time_shown.append(ap_time)
        # Process codes left
        codes_left_text = self.game_driver.get_codes_left_text(game_page)
        if codes_left_text is not None:
            for codes_left in config.show_codes_left:
                if codes_left == codes_left_text and codes_left not in self.codes_left_shown:
                    updates.append(CODES_LEFT_TEXT.format(codes=codes_left))
                    self.codes_left_shown.append(codes_left)
        # Process hints
        for hint_id in sorted(hints.keys()):
            if hint_id not in self.hints_shown and hint_id:
                self.hints_shown.append(hint_id)
                updates.append(NEW_HINT_MESSAGE.format(
                    hint_number=hint_id,
                    hint=hints[hint_id]))
        # Catch task was changed
        if self.last_task_text != task_text:
            self.last_task_text = task_text
            updates.append(TASK_EDITED_MESSAGE.format(task=task_text))
        # Codes try limited!!
        if self.game_driver.answer_limit(game_page) is not None and not self.codes_limit_shown:
            updates.append(self.game_driver.answer_limit(game_page))
            self.codes_limit_shown = True
        return self.replace_forbidden_words(updates)
