# -*- coding: utf-8 -*-
from time import sleep

from game.driver import GameDriver

MAX_ATTEMPTS = 5

REPLACE_DICTIONARY = {'<br/>': "\r\n"}


class GameWorker:
    last_level_shown = None
    last_hint_shown = None
    last_task_text = None

    def __init__(self):
        self.game_driver = GameDriver()

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
        while self.game_driver.logged_out(game_page) and attempt < MAX_ATTEMPTS:
            game_page = self.game_driver.login_user()
            attempt += 1
            sleep(1)
        if attempt >= MAX_ATTEMPTS:
            return
        task_text = self.game_driver.get_task(game_page)
        current_level = self.game_driver.get_level_params(game_page)
        hints = self.game_driver.get_all_hints(game_page)
        # TODO: rewrite to show bunch of hints!
        if self.last_level_shown != current_level["LevelNumber"] or self.last_level_shown is None:
            self.last_level_shown = current_level["LevelNumber"]
            self.last_hint_shown = None
            self.last_task_text = task_text
            updates.append(u"Новый уровень! \r\n {task}".format(task=task_text))
        if self.last_hint_shown != max(hints.keys()) or self.last_hint_shown is None:
            self.last_hint_shown = max(hints.keys())
            updates.append(u"Новая подсказка: \r\n {hint}".format(hint=hints[max(hints.keys())]))
        if self.last_task_text != task_text:
            self.last_task_text = task_text
            updates.append(u"Задание было изменено! \r\n {task}".format(task=task_text))
        return self.replace_forbidden_words(updates)
