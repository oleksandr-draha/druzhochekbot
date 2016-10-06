# -*- coding: utf-8 -*-
from time import sleep

from config.config import config
from config.dictionary import NEW_TASK_MESSAGE, NEW_HINT_MESSAGE, TASK_EDITED_MESSAGE
from game.driver import GameDriver

REPLACE_DICTIONARY = {'<br/>': "\r\n"}


class GameWorker:
    last_level_shown = None
    last_task_text = None
    hints_shown = []
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
        while not self.game_driver.is_logged(game_page) and attempt < config.max_game_attempts:
            game_page = self.game_driver.login_user()
            attempt += 1
            sleep(config.relogin_interval)
        if attempt >= config.max_game_attempts:
            return
        task_text = self.game_driver.get_task(game_page)
        if task_text is None:
            return
        current_level = self.game_driver.get_level_params(game_page)
        self.game_driver.set_level_params(game_page)
        hints = self.game_driver.get_all_hints(game_page)
        if self.last_level_shown != current_level["LevelNumber"] or self.last_level_shown is None:
            self.last_level_shown = current_level["LevelNumber"]
            self.hints_shown = []
            self.last_task_text = task_text
            updates.append(NEW_TASK_MESSAGE[0])
            updates.append(NEW_TASK_MESSAGE[1].format(
                level_number=current_level["LevelNumber"]))
            updates.append(NEW_TASK_MESSAGE[2].format(task=task_text))
        # TODO: rewrite to show bunch of hints!
        for hint_id in sorted(hints.keys()):
            if hint_id not in self.hints_shown and hint_id:
                self.hints_shown.append(hint_id)
                updates.append(NEW_HINT_MESSAGE.format(
                    hint_number=hint_id,
                    hint=hints[hint_id]))
        if self.last_task_text != task_text:
            self.last_task_text = task_text
            updates.append(TASK_EDITED_MESSAGE.format(task=task_text))
        return self.replace_forbidden_words(updates)
