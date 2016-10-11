# -*- coding: utf-8 -*-
from time import sleep

from config.config import config
from config.dictionary import NEW_TASK_MESSAGE, NEW_HINT_MESSAGE, TASK_EDITED_MESSAGE, CODES_LEFT_TEXT, TASK_MESSAGE, \
    HINTS_APPEND, LIMIT_APPEND, ORG_MESSAGE_APPEND
from game.driver import GameDriver

REPLACE_DICTIONARY = {u'<br/>': "\r\n",
                      u'**Автопереход**': u'<b>Автопереход</b>'}


class GameWorker:
    last_level_shown = None
    last_task_text = None
    ap_time_shown = []
    hints_time_shown = []
    codes_left_shown = []
    hints_shown = []
    connected = False
    finished_shown = False
    codes_limit_shown = False
    _request_task_text = False
    last_org_message_shown = None

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
            if update:
                for word, replace in REPLACE_DICTIONARY.iteritems():
                    update = update.replace(word, replace)
                replaced_updates.append(update)
        return replaced_updates

    def reset_level(self):
        self.last_level_shown = None
        self.last_task_text = None
        self.ap_time_shown = []
        self.hints_time_shown = []
        self.codes_left_shown = []
        self.hints_shown = []
        self.finished_shown = False
        self.codes_limit_shown = False

    def check_updates(self):
        updates = []
        game_page = self.game_driver.get_game_page()

        # TODO: Separate function:
        attempt = 0
        while not self.game_driver.is_logged(game_page) and attempt < config.max_game_attempts:
            self.game_driver.login_user()
            game_page = self.game_driver.get_game_page()
            attempt += 1
            sleep(config.relogin_interval)
        if attempt >= config.max_game_attempts:
            return

        if self.game_driver.is_finished(game_page):
            # If game is finished - updates should not be checked
            if not self.finished_shown:
                self.finished_shown = True
                updates.append(self.game_driver.get_finish_message(game_page))
            if self._request_task_text:
                self._request_task_text = False
                updates.append(self.game_driver.get_finish_message(game_page))
        else:
            task_text = self.game_driver.get_task(game_page)
            if task_text is None:
                return
            current_level = self.game_driver.set_level_params(game_page)
            hints = self.game_driver.get_all_hints(game_page)
            time_to_ap_text = self.game_driver.get_time_to_ap(game_page)
            time_to_hints_text = self.game_driver.get_time_to_hints(game_page)
            codes_left_text = self.game_driver.get_codes_left_text(game_page)
            org_message = self.game_driver.get_org_message(game_page)

            # If new task was received:
            if self.last_level_shown != current_level["LevelNumber"]:
                self.reset_level()
                self.last_level_shown = current_level["LevelNumber"]
                self.last_task_text = task_text
                updates.append(NEW_TASK_MESSAGE.format(
                    level_number=current_level["LevelNumber"],
                    task=task_text))
            # If task text was requested
            if self._request_task_text:
                self._request_task_text = False
                updates.append(TASK_MESSAGE.format(
                    level_number=current_level["LevelNumber"],
                    task=task_text))
            # Process AP time
            if time_to_ap_text is not None:
                if config.show_first_ap_time and "first" not in self.ap_time_shown:
                    updates.append(time_to_ap_text)
                    self.ap_time_shown.append("first")
                for ap_time in config.show_time_left_minutes:
                    minute_locator = u" {minutes} минут".format(minutes=ap_time)
                    hour = u"час "
                    if minute_locator in time_to_ap_text and hour not in time_to_ap_text and ap_time not in self.ap_time_shown:
                        # Not to show duplicate AP texts:
                        if time_to_ap_text not in updates:
                            updates.append(time_to_ap_text)
                        self.ap_time_shown.append(ap_time)
            # Process hints
            hint_will_be_shown = False
            for hint_id in sorted(hints.keys()):
                if hint_id not in self.hints_shown and hint_id:
                    self.hints_shown.append(hint_id)
                    updates.append(NEW_HINT_MESSAGE.format(
                        smile=HINTS_APPEND,
                        hint_number=hint_id,
                        hint=hints[hint_id]))
                    hint_will_be_shown = True
            if hint_will_be_shown and len(time_to_hints_text):
                updates.append(time_to_hints_text[0])
                if "first" not in self.hints_time_shown:
                    self.hints_time_shown.append("first")
            # Process hints time
            if len(time_to_hints_text):
                if config.show_first_hint_time and "first" not in self.hints_time_shown:
                    updates.append(time_to_hints_text[0])
                    self.hints_time_shown.append("first")
                # Should we show how much time left before next hint?
                if config.show_time_to_hint:
                    for hint_time in config.show_time_left_minutes:
                        minute_locator = u" {minutes} минут".format(minutes=hint_time)
                        hour = u"час "
                        time_to_hint_text = time_to_hints_text[0]
                        if minute_locator in time_to_hint_text \
                                and hour not in time_to_hint_text \
                                and hint_time not in self.hints_time_shown:
                            # Not to show duplicate Hints texts:
                            if time_to_hint_text not in updates:
                                updates.append(time_to_hint_text)
                            self.hints_time_shown.append(hint_time)
            # Process codes left
            if codes_left_text is not None:
                for codes_left in config.show_codes_left:
                    if codes_left == codes_left_text and codes_left not in self.codes_left_shown:
                        if CODES_LEFT_TEXT.get(codes_left) is not None:
                                updates.append(CODES_LEFT_TEXT.get(codes_left).format(codes=codes_left))
                                self.codes_left_shown.append(codes_left)
                        else:
                            updates.append(CODES_LEFT_TEXT['all'].format(codes=codes_left))
                            self.codes_left_shown.append(codes_left)
            # Catch task was changed
            if self.last_task_text != task_text:
                self.last_task_text = task_text
                updates.append(TASK_EDITED_MESSAGE.format(task=task_text))
            # Codes try limited!!
            if self.game_driver.answer_limit(game_page) is not None and not self.codes_limit_shown:
                updates.append(LIMIT_APPEND + self.game_driver.answer_limit(game_page))
                self.codes_limit_shown = True
            # Message from ORGANIZATORS received:
            if org_message != self.last_org_message_shown and org_message is not None:
                updates.append(ORG_MESSAGE_APPEND + org_message)
                self.last_org_message_shown = org_message
        return self.replace_forbidden_words(updates)
