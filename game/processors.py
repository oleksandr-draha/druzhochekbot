# -*- coding: utf-8 -*-
from time import sleep

from config import bot_settings, game_settings, timeouts, tasks_log
from config.dictionary import Smiles, GameMessages
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
    finished_shown = False
    not_started_shown = False
    about_to_start_shown = False
    closed_shown = False
    banned_as_bot_shown = False
    not_payed_shown = False
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
        self.codes_left_text_shown = []
        self.hints_shown = []
        self.finished_shown = False
        self.not_payed_shown = False
        self.not_started_shown = False
        self.about_to_start_shown = False
        self.closed_shown = False
        self.banned_as_bot_shown = False
        self.codes_limit_shown = False

    def process_user_was_not_logged(self):
        attempt = 0
        while not self.game_driver.is_logged(self.game_page) and attempt < timeouts.max_game_attempts:
            self.game_driver.login_user()
            self.game_page = self.game_driver.get_game_page()
            attempt += 1
            if attempt >= timeouts.max_game_attempts:
                return True
            sleep(timeouts.relogin_interval)
        return False

    def process_game_not_payed(self):
        updates = []
        if self.game_driver.not_payed(self.game_page):
            if not self.not_payed_shown:
                self.not_payed_shown = True
                updates.append(self.game_driver.not_payed(self.game_page))
        return updates

    def process_game_not_started(self):
        updates = []
        if self.game_driver.not_started(self.game_page):
            if not self.not_started_shown:
                self.not_started_shown = True
                updates.append(self.game_driver.get_not_started_message(self.game_page))
        return updates

    def process_game_about_to_start(self):
        updates = []
        if self.game_driver.about_to_start(self.game_page):
            if not self.about_to_start_shown:
                self.about_to_start_shown = True
                updates.append(self.game_driver.get_about_to_start_message(self.game_page))
        return updates

    def process_game_closed(self):
        updates = []
        if self.game_driver.closed(self.game_page):
            if not self.closed_shown:
                self.closed_shown = True
                updates.append(self.game_driver.get_closed_message(self.game_page))
            bot_settings.paused = True
        return updates

    def process_banned_as_bot(self):
        updates = []
        if self.game_driver.banned_as_bot(self.game_page):
            if not self.banned_as_bot_shown:
                self.banned_as_bot_shown = True
                updates.append(self.game_driver.get_banned_as_bot_message(self.game_page))
            bot_settings.paused = True
        else:
            self.banned_as_bot_shown = False
        return updates

    def process_game_finished(self):
        updates = []
        if self.game_driver.is_finished(self.game_page):
            # If game is finished - updates should not be checked
            if not self.finished_shown:
                self.finished_shown = True
                updates.append(self.game_driver.get_finish_message(self.game_page))
            bot_settings.paused = True
        return updates

    def process_new_task_received(self):
        updates = []
        current_level = self.game_driver.set_level_params(self.game_page)
        task_text = self.game_driver.get_task(self.game_page)
        if self.last_level_shown != current_level["LevelNumber"]:
            self.reset_level()
            self.last_level_shown = current_level["LevelNumber"]
            self.last_task_text = task_text
            updates.append(GameMessages.NEW_TASK.format(
                level_number=current_level["LevelNumber"],
                task=task_text))
            tasks_log.log_task(current_level["LevelNumber"], self.game_page)
        return updates

    def process_ap_time(self):
        updates = []
        time_to_ap_text = self.game_driver.get_time_to_ap(self.game_page)
        if time_to_ap_text is not None:
            if game_settings.show_first_ap_time and "first" not in self.ap_time_shown:
                updates.append(Smiles.AP + time_to_ap_text)
                self.ap_time_shown.append("first")
            for ap_time in game_settings.show_time_left_minutes:
                minute_locator = u" {minutes} минут".format(minutes=ap_time)
                hour = u"час "
                if minute_locator in time_to_ap_text and hour not in time_to_ap_text and ap_time not in self.ap_time_shown:
                    # Not to show duplicate AP texts:
                    if time_to_ap_text not in updates:
                        updates.append(Smiles.AP + time_to_ap_text)
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
                updates.append(GameMessages.NEW_HINT.format(
                    smile=Smiles.HINTS,
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
            if game_settings.show_first_hint_time and "first" not in self.hints_time_shown:
                updates.append(time_to_hints_text[0])
                self.hints_time_shown.append("first")
            # Should we show how much time left before next hint?
            if game_settings.show_time_to_hint:
                for hint_time in game_settings.show_time_left_minutes:
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
            for codes_left in game_settings.show_codes_left:
                if codes_left_text <= codes_left \
                        and codes_left not in self.codes_left_shown \
                        and codes_left_text not in self.codes_left_text_shown:
                    # Prepare message to show:
                    if GameMessages.CODES_LEFT_TEXT.get(codes_left_text) is not None:
                        updates.append(GameMessages.CODES_LEFT_TEXT.get(codes_left_text).format(codes=codes_left_text))
                    else:
                        updates.append(GameMessages.CODES_LEFT_TEXT['all'].format(codes=codes_left_text))
                    # Prevent from showing duplicate messages:
                    for codes_number in game_settings.show_codes_left:
                        if codes_number >= codes_left:
                            self.codes_left_shown.append(codes_number)
                    self.codes_left_text_shown.append(codes_left_text)
        return updates

    def process_tries_limit(self):
        updates = []
        if self.game_driver.answer_limit(self.game_page) is not None:
            if not self.codes_limit_shown:
                updates.append(Smiles.LIMIT + self.game_driver.answer_limit(self.game_page))
                self.codes_limit_shown = True
                if bot_settings.autohandbrake:
                    self.game_driver.auto_handbrake = True
        else:
            self.game_driver.auto_handbrake = False
        return updates

    def process_org_message(self):
        updates = []
        org_message = self.game_driver.get_org_message(self.game_page)
        if org_message != self.last_org_message_shown and org_message is not None:
            updates.append(Smiles.ORG_MESSAGE + org_message)
            self.last_org_message_shown = org_message
        return updates

    def process_task_was_changed(self):
        updates = []
        level_number = self.game_driver.set_level_params(self.game_page)["LevelNumber"]
        task_text = self.game_driver.get_task(self.game_page)
        if self.last_task_text != task_text:
            self.last_task_text = task_text
            updates.append(GameMessages.TASK_EDITED.format(task=task_text))
            tasks_log.log_task(level_number, self.game_page)
        return updates
