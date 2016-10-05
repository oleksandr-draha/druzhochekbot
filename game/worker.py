# -*- coding: utf-8 -*-
from time import sleep

from game.driver import GameDriver

# TODO: To config or class attributes?
from telegram.dictionary import NEW_TASK_MESSAGE, NEW_HINT_MESSAGE, TASK_EDITED_MESSAGE

MAX_ATTEMPTS = 5

REPLACE_DICTIONARY = {'<br/>': "\r\n"}


class GameWorker:
    last_level_shown = None
    last_hint_shown = None
    last_task_text = None
    connected = False

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

    def check_updates(self):
        updates = []
        game_page = self.game_driver.get_game_page()
        attempt = 0
        while not self.game_driver.is_logged(game_page) and attempt < MAX_ATTEMPTS:
            game_page = self.game_driver.login_user()
            attempt += 1
            sleep(1)
        if attempt >= MAX_ATTEMPTS:
            return
        task_text = self.game_driver.get_task(game_page)
        if task_text is None:
            return
        current_level = self.game_driver.get_level_params(game_page)
        hints = self.game_driver.get_all_hints(game_page)
        if self.last_level_shown != current_level["LevelNumber"] or self.last_level_shown is None:
            self.last_level_shown = current_level["LevelNumber"]
            self.last_hint_shown = None
            self.last_task_text = task_text
            updates.append(NEW_TASK_MESSAGE.format(
                level_number=current_level["LevelNumber"],
                task=task_text))
        # TODO: rewrite to show bunch of hints!
        if self.last_hint_shown != max(hints.keys()) or self.last_hint_shown is None:
            self.last_hint_shown = max(hints.keys())
            updates.append(NEW_HINT_MESSAGE.format(
                hint_number=max(hints.keys()),
                hint=hints[max(hints.keys())]))
        if self.last_task_text != task_text:
            self.last_task_text = task_text
            updates.append(TASK_EDITED_MESSAGE.format(task=task_text))
        return self.replace_forbidden_words(updates)
