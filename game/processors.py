# -*- coding: utf-8 -*-
from time import sleep

from config import config
from config.dictionary import CODES_LEFT_TEXT, NEW_TASK_MESSAGE, AP_MESSAGE_APPEND, NEW_HINT_MESSAGE, \
    HINTS_APPEND, LIMIT_APPEND, ORG_MESSAGE_APPEND, TASK_EDITED_MESSAGE
from game.driver import GameDriver


class GameProcessor:
    game_page = None
    last_level_shown = None
    last_task_text = None
    all_hints = {}
    ap_time_shown = []
    hints_time_shown = []
    codes_left_shown = []
    codes_left_text_shown = []
    hints_shown = []
    connected = False
    finished_shown = False
    not_started_shown = False
    codes_limit_shown = False
    _request_task_text = False
    last_org_message_shown = None
    tasks_received = {}

    def __init__(self):
        self.game_driver = GameDriver()
        self.connected = self.game_driver.connected

    def reset_level(self):
        self.last_level_shown = None
        self.last_task_text = None
        self.all_hints = {}
        self.ap_time_shown = []
        self.hints_time_shown = []
        self.codes_left_shown = []
        self.hints_shown = []
        self.finished_shown = False
        self.not_started_shown = False
        self.codes_limit_shown = False

    def process_user_was_not_logged(self):
        attempt = 0
        while not self.game_driver.is_logged(self.game_page) and attempt < config.max_game_attempts:
            self.game_driver.login_user()
            self.game_page = self.game_driver.get_game_page()
            attempt += 1
            if attempt >= config.max_game_attempts:
                return True
            sleep(config.relogin_interval)
        return False

    def process_game_not_started(self):
        updates = []
        if self.game_driver.not_started(self.game_page):
            if not self.not_started_shown:
                self.not_started_shown = True
                updates.append(self.game_driver.get_not_started_message(self.game_page))
        return updates

    def process_game_finished(self):
        updates = []
        if self.game_driver.is_finished(self.game_page):
            # If game is finished - updates should not be checked
            if not self.finished_shown:
                self.finished_shown = True
                updates.append(self.game_driver.get_finish_message(self.game_page))
            if self._request_task_text:
                self._request_task_text = False
                updates.append(self.game_driver.get_finish_message(self.game_page))
        return updates

    def process_new_task_received(self):
        updates = []
        current_level = self.game_driver.set_level_params(self.game_page)
        task_text = self.game_driver.get_task(self.game_page)
        if self.last_level_shown != current_level["LevelNumber"]:
            self.reset_level()
            self.last_level_shown = current_level["LevelNumber"]
            self.last_task_text = task_text
            updates.append(NEW_TASK_MESSAGE.format(
                level_number=current_level["LevelNumber"],
                task=task_text))
            self.tasks_received.setdefault(current_level["LevelNumber"], task_text)
        return updates

    def process_ap_time(self):
        updates = []
        time_to_ap_text = self.game_driver.get_time_to_ap(self.game_page)
        if time_to_ap_text is not None:
            if config.show_first_ap_time and "first" not in self.ap_time_shown:
                updates.append(AP_MESSAGE_APPEND + time_to_ap_text)
                self.ap_time_shown.append("first")
            for ap_time in config.show_time_left_minutes:
                minute_locator = u" {minutes} минут".format(minutes=ap_time)
                hour = u"час "
                if minute_locator in time_to_ap_text and hour not in time_to_ap_text and ap_time not in self.ap_time_shown:
                    # Not to show duplicate AP texts:
                    if time_to_ap_text not in updates:
                        updates.append(AP_MESSAGE_APPEND + time_to_ap_text)
                    self.ap_time_shown.append(ap_time)
        return updates

    def process_hints(self):
        updates = []
        hint_will_be_shown = False
        hints = self.game_driver.get_all_hints(self.game_page)
        self.all_hints = hints
        time_to_hints_text = self.game_driver.get_time_to_hints(self.game_page)
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
        return updates

    def process_hints_time(self):
        updates = []
        time_to_hints_text = self.game_driver.get_time_to_hints(self.game_page)
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
        return updates

    def process_codes_left(self):
        updates = []
        codes_left_text = self.game_driver.get_codes_left_text(self.game_page)
        if codes_left_text is not None:
            for codes_left in config.show_codes_left:
                if codes_left_text <= codes_left \
                        and codes_left not in self.codes_left_shown \
                        and codes_left_text not in self.codes_left_text_shown:
                    # Prepare message to show:
                    if CODES_LEFT_TEXT.get(codes_left_text) is not None:
                        updates.append(CODES_LEFT_TEXT.get(codes_left_text).format(codes=codes_left_text))
                    else:
                        updates.append(CODES_LEFT_TEXT['all'].format(codes=codes_left_text))
                    # Prevent from showing duplicate messages:
                    for codes_number in config.show_codes_left:
                        if codes_number >= codes_left:
                            self.codes_left_shown.append(codes_number)
                    self.codes_left_text_shown.append(codes_left_text)
        return updates

    def process_tries_limit(self):
        updates = []
        if self.game_driver.answer_limit(self.game_page) is not None and not self.codes_limit_shown:
            updates.append(LIMIT_APPEND + self.game_driver.answer_limit(self.game_page))
            self.codes_limit_shown = True
        return updates

    def process_org_message(self):
        updates = []
        org_message = self.game_driver.get_org_message(self.game_page)
        if org_message != self.last_org_message_shown and org_message is not None:
            updates.append(ORG_MESSAGE_APPEND + org_message)
            self.last_org_message_shown = org_message
        return updates

    def process_task_was_changed(self):
        updates = []
        level_number = self.game_driver.set_level_params(self.game_page)["LevelNumber"]
        task_text = self.game_driver.get_task(self.game_page)
        if self.last_task_text != task_text:
            self.last_task_text = task_text
            updates.append(TASK_EDITED_MESSAGE.format(task=task_text))
            self.tasks_received[level_number] = task_text
        return updates
