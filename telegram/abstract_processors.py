# -*- coding: utf-8 -*-
from config import bot_settings
from config.dictionary import SettingsMessages, CommonMessages
from game.worker import GameWorker
from telegram.driver import TelegramDriver


class AbstractProcessors(TelegramDriver):
    stopped = False

    def __init__(self):
        super(AbstractProcessors, self).__init__()
        self.game_worker = None
        self._load_settings()

    def _reset(self):
        self.get_updates()
        bot_settings.paused = True
        self.game_worker = None
        self._load_settings()

    def _load_settings(self):
        self.game_worker = GameWorker()
        if self.game_worker.connected:
            if bot_settings.group_chat_id is None:
                self.admin_message(CommonMessages.CONNECTION_OK_MESSAGES)
                self.admin_message(CommonMessages.PLEASE_APPROVE_MESSAGES)
            return True
        else:
            self.admin_message(SettingsMessages.CONNECTION_PROBLEM)
            self.admin_message(SettingsMessages.CHECK_SETTINGS)
            return False

    def _admin_command(self, message, do_function):
        from_id = message["from_id"]
        chat_id = message["chat_id"]
        if bot_settings.is_admin(from_id):
            if chat_id < 0:
                if chat_id == bot_settings.group_chat_id:
                    self.answer_message(message, CommonMessages.NOT_FOR_GROUP_CHAT_MESSAGES)
                else:
                    self.answer_message(message, CommonMessages.NO_GROUP_CHAT_MESSAGES)
            else:
                do_function(message)
        elif bot_settings.answer_forbidden:
            self.answer_message(message, CommonMessages.ACCESS_VIOLATION_MESSAGES)

    def _admin_in_group_chat_command(self, message, do_function):
        from_id = message["from_id"]
        chat_id = message["chat_id"]
        if bot_settings.is_admin(from_id):
            if chat_id < 0:
                if chat_id == bot_settings.group_chat_id:
                    do_function(message)
                else:
                    self.answer_message(message, CommonMessages.NO_GROUP_CHAT_MESSAGES)
            else:
                do_function(message)
        elif bot_settings.answer_forbidden:
            self.answer_message(message, CommonMessages.ACCESS_VIOLATION_MESSAGES)

    def _user_command(self, message, do_function):
        from_id = message["from_id"]
        chat_id = message["chat_id"]
        if chat_id < 0:
            if chat_id == bot_settings.group_chat_id:
                do_function(message)
            elif bot_settings.is_admin(from_id):
                self.answer_message(message, CommonMessages.NO_GROUP_CHAT_MESSAGES)
            elif bot_settings.answer_forbidden:
                self.answer_message(message, CommonMessages.ACCESS_VIOLATION_MESSAGES)
        elif bot_settings.is_user(from_id):
            do_function(message)
        elif bot_settings.answer_forbidden:
            self.answer_message(message, CommonMessages.ACCESS_VIOLATION_MESSAGES)
