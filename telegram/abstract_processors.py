from config import config
from config.dictionary import CONNECTION_OK_MESSAGES, PLEASE_APPROVE_MESSAGES, CONNECTION_PROBLEM_MESSAGES, \
    CHECK_SETTINGS_MESSAGES, NOT_FOR_GROUP_CHAT_MESSAGES, NO_GROUP_CHAT_MESSAGES, ACCESS_VIOLATION_MESSAGES
from game.driver import GameDriver
from game.worker import GameWorker
from telegram.driver import TelegramDriver


class AbstractProcessors(TelegramDriver):
    def __init__(self):
        super(AbstractProcessors, self).__init__()
        self.paused = False
        self.stopped = False
        self.game_worker = None
        self.group_chat_id = None
        self.unknown_users = []
        self._load_settings()

    def _reset(self):
        self.get_updates()
        self.paused = True
        self.stopped = False
        self.game_worker = None
        self.group_chat_id = None
        self._load_settings()

    def _load_settings(self):
        GameDriver.login = config.game_login
        GameDriver.password = config.game_password
        GameDriver.game_id = config.game_id
        GameDriver.host = config.game_host

        self.group_chat_id = config.group_chat_id
        self.paused = config.paused
        self.game_worker = GameWorker()
        if self.game_worker.connected:
            if self.group_chat_id is None:
                self.admin_message(CONNECTION_OK_MESSAGES)
                self.admin_message(PLEASE_APPROVE_MESSAGES)
            return True
        else:
            self.admin_message(CONNECTION_PROBLEM_MESSAGES)
            self.admin_message(CHECK_SETTINGS_MESSAGES)
            return False

    def _admin_command(self, message, do_function):
        from_id = message["from_id"]
        chat_id = message["chat_id"]
        if config.is_admin(from_id):
            if chat_id < 0:
                if chat_id == self.group_chat_id:
                    self.answer_message(message, NOT_FOR_GROUP_CHAT_MESSAGES)
                else:
                    self.answer_message(message, NO_GROUP_CHAT_MESSAGES)
            else:
                do_function(message)
        elif config.answer_forbidden:
            self.answer_message(message, ACCESS_VIOLATION_MESSAGES)

    def _admin_in_group_chat_command(self, message, do_function):
        from_id = message["from_id"]
        chat_id = message["chat_id"]
        if config.is_admin(from_id):
            if chat_id < 0:
                if chat_id == self.group_chat_id:
                    do_function(message)
                else:
                    self.answer_message(message, NO_GROUP_CHAT_MESSAGES)
            else:
                do_function(message)
        elif config.answer_forbidden:
            self.answer_message(message, ACCESS_VIOLATION_MESSAGES)

    def _user_command(self, message, do_function):
        from_id = message["from_id"]
        chat_id = message["chat_id"]
        if chat_id < 0:
            if chat_id == self.group_chat_id:
                do_function(message)
            elif config.is_admin(from_id):
                self.answer_message(message, NO_GROUP_CHAT_MESSAGES)
            elif config.answer_forbidden:
                self.answer_message(message, ACCESS_VIOLATION_MESSAGES)
        elif config.is_user(from_id):
            do_function(message)
        elif config.answer_forbidden:
            self.answer_message(message, ACCESS_VIOLATION_MESSAGES)
