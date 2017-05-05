# -*- coding: utf-8 -*-
import json
import time

from config.config import config
from config.dictionary import PAUSED_MESSAGE, LETS_GO_MESSAGES, START_PAUSE_MESSAGES, \
    RESUME_MESSAGE, END_PAUSE_MESSAGES, BYE_MESSAGES, NO_CODE_FOUND_MESSAGE, GIVE_ME_LOGIN, GIVE_ME_PASSWORD, \
    GIVE_ME_HOST, GIVE_ME_GAME, AFFIRMATIVE_MESSAGES, NOT_GROUP_CHAT_MESSAGES, CONNECTION_PROBLEM_MESSAGES, \
    CONNECTION_OK_MESSAGES, PLEASE_APPROVE_MESSAGES, ACCESS_VIOLATION_MESSAGES, \
    ALREADY_PAUSED_MESSAGE, UNKNOWN_MESSAGES, STATUS_MESSAGE, \
    PAUSED_STATUS_MESSAGES, GAME_CONNECTION_MESSAGES, INFO_MESSAGE, NOT_FOR_GROUP_CHAT_MESSAGES, NO_GROUP_CHAT_MESSAGES, \
    DISAPPROVE_MESSAGES, BOT_WAS_RESET_MESSAGE, ADMIN_HELP_MESSAGE, CHECK_SETTINGS_MESSAGES, \
    SETTINGS_WERE_CHANGED_MESSAGES, \
    SETTINGS_WERE_SAVED_MESSAGES, SETTINGS_WERE_NOT_SAVED_MESSAGES, REGULAR_HELP_MESSAGE, \
    GAME_FINISHED_MESSAGE, CODES_BLOCKED_MESSAGE, NEW_USER_WAS_ADDED, DUPLICATE_USER_ID, TASK_MESSAGE, \
    NEW_HINT_MESSAGE, HINTS_APPEND, WRONG_USER_ID_MESSAGE, USER_DELETED_MESSAGE, CANNOT_DELETE_ADMIN_MESSAGE, \
    DELETE_USER_ID_MESSAGE, ENTER_NEW_PASS, PASS_WAS_CHANGED, DUPLICATE_PASS
from game.driver import GameDriver
from game.worker import GameWorker
from telegram.driver import TelegramDriver


class TelegramWorker:
    def __init__(self):
        self.telegram_driver = TelegramDriver()
        self.telegram_driver.get_updates()
        self.initial_message = None
        self.initialize_attempts = 0
        self.paused = False
        self.stopped = False
        self.game_worker = None
        self.group_chat_id = None
        self.add_admin_passphrase = None
        self.add_field_passphrase = None
        self.add_kc_passphrase = None

        # Messages dictionary

        self.load_settings()

    @staticmethod
    def _is_admin(from_id):
        return from_id in config.admin_ids

    @staticmethod
    def _is_field(from_id):
        return from_id in config.field_ids

    @staticmethod
    def _is_kc(from_id):
        return from_id in config.kc_ids

    def get_usernames(self, users):
        usernames = {}
        for user in users:
            usernames.setdefault(user, self.telegram_driver.get_username(user))
        return usernames

    def load_settings(self):
        GameDriver.login = config.game_login
        GameDriver.password = config.game_password
        GameDriver.game_id = config.game_id
        GameDriver.host = config.game_host
        self.game_worker = GameWorker()
        if self.game_worker.connected:
            self.telegram_driver.admin_message(CONNECTION_OK_MESSAGES)
            self.telegram_driver.admin_message(PLEASE_APPROVE_MESSAGES)
            return True
        else:
            self.telegram_driver.admin_message(CONNECTION_PROBLEM_MESSAGES)
            self.telegram_driver.admin_message(CHECK_SETTINGS_MESSAGES)
            return False

    def check_answer_from_chat_id(self, chat_id):
        for message in self.check_new_messages():
            if message["from_id"] == chat_id:
                return message

    def check_answer_with_passphrase(self, passphrase):
        for message in self.check_new_messages():
            if message["text"] == passphrase or message["text"] == config.cancel_command:
                return message

    def wait_for_answer(self, from_id):
        """
        Wait for message from specified id
        :param from_id: int
        :return:
        :rtype: dict
        """
        while True:
            answer = self.check_answer_from_chat_id(from_id)
            if answer is None:
                time.sleep(config.answer_check_interval)
                continue
            return answer

    def wait_for_message_from_new_user(self, passphrase):
        """
        Wait for message from new user (it could be anyone)
        :param passphrase: str
        :return:
        :rtype: dict
        """
        while True:
            answer = self.check_answer_with_passphrase(passphrase)
            if answer is None:
                time.sleep(config.answer_check_interval)
                continue
            return answer

    def check_new_messages(self):
        """
        Checks whether new text messages present in the channel
        :return:
        :rtype: list of dict
        """
        messages = []
        for message in self.telegram_driver.get_updates():
            if message.get('message', {}).get('text') is not None:
                messages.append(
                    {'id': message.get('message', {}).get('message_id'),
                     'text': message.get('message', {}).get('text'),
                     'from_id': message.get('message', {}).get('from', {}).get('id'),
                     'chat_id': message.get('message', {}).get('chat', {}).get('id')})
        return messages

    def admin_command(self, message, do_function):
        from_id = message["from_id"]
        chat_id = message["chat_id"]
        if self._is_admin(from_id):
            if chat_id < 0:
                if chat_id == self.group_chat_id:
                    self.telegram_driver.answer_message(message, NOT_FOR_GROUP_CHAT_MESSAGES)
                else:
                    self.telegram_driver.answer_message(message, NO_GROUP_CHAT_MESSAGES)
            else:
                do_function(message)
        elif config.answer_forbidden:
            self.telegram_driver.answer_message(message, ACCESS_VIOLATION_MESSAGES)

    def user_command(self, message, do_function):
        from_id = message["from_id"]
        chat_id = message["chat_id"]
        if chat_id < 0:
            if chat_id == self.group_chat_id:
                do_function(message)
            elif self._is_admin(from_id):
                self.telegram_driver.answer_message(message, NO_GROUP_CHAT_MESSAGES)
            elif config.answer_forbidden:
                self.telegram_driver.answer_message(message, ACCESS_VIOLATION_MESSAGES)
        elif self._is_admin(from_id):
            do_function(message)
        elif config.answer_forbidden:
            self.telegram_driver.answer_message(message, ACCESS_VIOLATION_MESSAGES)

    def check_codes(self, message, command):
        codes = message["text"].replace(command, '').rstrip().lstrip().split()
        results = NO_CODE_FOUND_MESSAGE
        if len(codes):
            results = ''
            for code in codes:
                results += self.game_worker.game_driver.try_code(code)
                if results in [CODES_BLOCKED_MESSAGE, GAME_FINISHED_MESSAGE]:
                    return results
        return results

    def check_code(self, message, command):
        code = message["text"].replace(command, '').rstrip().lstrip()
        results = NO_CODE_FOUND_MESSAGE
        if len(code):
            results = self.game_worker.game_driver.try_code(code)
        return results

    @staticmethod
    def get_command(message):
        return message["text"].split()[0].split('@')[0]

    def _do_stop(self, message):
        self.telegram_driver.answer_message(message, BYE_MESSAGES)
        self.stopped = True

    def _do_pause(self, message):
        if not self.paused:
            self.telegram_driver.answer_message(message, START_PAUSE_MESSAGES)
            self.paused = True
        else:
            self.telegram_driver.answer_message(message, ALREADY_PAUSED_MESSAGE)

    def _do_resume(self, message):
        if self.paused:
            self.telegram_driver.answer_message(message, END_PAUSE_MESSAGES)
            self.paused = False
        else:
            self.telegram_driver.answer_message(message, RESUME_MESSAGE)

    def _do_codes(self, message):
        if not self.paused:
            command = self.get_command(message)
            result = self.check_codes(message, command)
            self.telegram_driver.answer_message(message, result)
        else:
            self.telegram_driver.answer_message(message, PAUSED_MESSAGE)

    def _do_code(self, message):
        if not self.paused:
            command = self.get_command(message)
            result = self.check_code(message, command)
            self.telegram_driver.answer_message(message, result)
        else:
            self.telegram_driver.answer_message(message, PAUSED_MESSAGE)

    def _do_approve(self, message):
        chat_id = message["chat_id"]
        self.telegram_driver.answer_message(message, LETS_GO_MESSAGES)
        self.group_chat_id = chat_id
        self.paused = False

    def approve_command(self, message):
        from_id = message["from_id"]
        chat_id = message["chat_id"]
        if self._is_admin(from_id):
            if chat_id < 0:
                self._do_approve(message)
            else:
                self.telegram_driver.answer_message(message, NOT_GROUP_CHAT_MESSAGES)
        elif config.answer_forbidden:
            self.telegram_driver.answer_message(message, ACCESS_VIOLATION_MESSAGES)

    def _do_add_admin(self, message):
        if len(message["text"].split()) > 1:
            admin_to_add = message["text"].split()[1]
            if not admin_to_add.isdigit():
                self.telegram_driver.answer_message(message, WRONG_USER_ID_MESSAGE)
            else:
                if self._is_admin(int(admin_to_add)):
                    self.telegram_driver.answer_message(
                        message,
                        DUPLICATE_USER_ID)
                else:
                    config.add_admin_id(int(admin_to_add))
                    self.telegram_driver.admin_message(
                        NEW_USER_WAS_ADDED.format(user_id=int(admin_to_add)))
                    # else:
                    #     self.telegram_driver.send_message(
                    #         from_id,
                    #         CREATE_PASSPHRASE_FOR_ADD_USER)
                    #     self.add_admin_passphrase = self.wait_for_answer(from_id)["text"]
                    #     self.telegram_driver.answer_message(message, WAITING_FOR_NEW_USER)
                    #     new_user_message = self.wait_for_message_from_new_user(self.add_admin_passphrase)
                    #     if new_user_message["text"] != config.cancel_command:
                    #         if self._is_admin(new_user_message["from_id"]):
                    #             self.telegram_driver.answer_message(
                    #                 new_user_message,
                    #                 DUPLICATE_USER_ID)
                    #         else:
                    #             config.add_admin_id(new_user_message["from_id"])
                    #             self.telegram_driver.admin_message(
                    #                 NEW_USER_WAS_ADDED.format(user_id=new_user_message["from_id"]))
                    #     else:
                    #         self.telegram_driver.answer_message(message, WAITING_FOR_NEW_USER_WAS_CANCELED)
                    #
                    #     self.add_admin_passphrase = None

    def _do_add_field(self, message):
        # from_id = message["from_id"]
        if len(message["text"].split()) > 1:
            field_to_add = message["text"].split()[1]
            if not field_to_add.isdigit():
                self.telegram_driver.answer_message(message, WRONG_USER_ID_MESSAGE)
            else:
                if self._is_field(int(field_to_add)):
                    self.telegram_driver.answer_message(
                        message,
                        DUPLICATE_USER_ID)
                else:
                    config.add_field_id(int(field_to_add))
                    self.telegram_driver.admin_message(
                        NEW_USER_WAS_ADDED.format(user_id=int(field_to_add)))
                    # else:
                    #     self.telegram_driver.send_message(
                    #         from_id,
                    #         CREATE_PASSPHRASE_FOR_ADD_USER)
                    #     self.add_field_passphrase = self.wait_for_answer(from_id)["text"]
                    #     self.telegram_driver.answer_message(message, WAITING_FOR_NEW_USER)
                    #     new_user_message = self.wait_for_message_from_new_user(self.add_field_passphrase)
                    #     if new_user_message["text"] != config.cancel_command:
                    #         if self._is_field(new_user_message["from_id"]):
                    #             self.telegram_driver.answer_message(
                    #                 new_user_message,
                    #                 DUPLICATE_USER_ID)
                    #         else:
                    #             config.add_field_id(new_user_message["from_id"])
                    #             self.telegram_driver.admin_message(
                    #                 NEW_USER_WAS_ADDED.format(user_id=new_user_message["from_id"]))
                    #     else:
                    #         self.telegram_driver.answer_message(message, WAITING_FOR_NEW_USER_WAS_CANCELED)
                    #
                    #     self.add_field_passphrase = None

    def _do_add_kc(self, message):
        # from_id = message["from_id"]
        if len(message["text"].split()) > 1:
            kc_to_add = message["text"].split()[1]
            if not kc_to_add.isdigit():
                self.telegram_driver.answer_message(message, WRONG_USER_ID_MESSAGE)
            else:
                if self._is_kc(int(kc_to_add)):
                    self.telegram_driver.answer_message(
                        message,
                        DUPLICATE_USER_ID)
                else:
                    config.add_kc_id(int(kc_to_add))
                    self.telegram_driver.admin_message(
                        NEW_USER_WAS_ADDED.format(user_id=int(kc_to_add)))
                    # else:
                    #     self.telegram_driver.send_message(
                    #         from_id,
                    #         CREATE_PASSPHRASE_FOR_ADD_USER)
                    #     self.add_kc_passphrase = self.wait_for_answer(from_id)["text"]
                    #     self.telegram_driver.answer_message(message, WAITING_FOR_NEW_USER)
                    #     new_user_message = self.wait_for_message_from_new_user(self.add_kc_passphrase)
                    #     if new_user_message["text"] != config.cancel_command:
                    #         if self._is_kc(new_user_message["from_id"]):
                    #             self.telegram_driver.answer_message(
                    #                 new_user_message,
                    #                 DUPLICATE_USER_ID)
                    #         else:
                    #             config.add_kc_id(new_user_message["from_id"])
                    #             self.telegram_driver.admin_message(
                    #                 NEW_USER_WAS_ADDED.format(user_id=new_user_message["from_id"]))
                    #     else:
                    #         self.telegram_driver.answer_message(message, WAITING_FOR_NEW_USER_WAS_CANCELED)
                    #
                    #     self.add_kc_passphrase = None

    def _do_delete_admin(self, message):
        from_id = message["from_id"]
        if len(config.admin_ids) == 1:
            self.telegram_driver.answer_message(message, CANNOT_DELETE_ADMIN_MESSAGE)
        else:
            if len(message["text"].split()) > 1:
                admin_to_delete = message["text"].split()[1]
            else:
                self.telegram_driver.answer_message(message, DELETE_USER_ID_MESSAGE)
                admin_to_delete = self.wait_for_answer(from_id)["text"]
            if not admin_to_delete.isdigit() or int(admin_to_delete) not in config.admin_ids:
                self.telegram_driver.answer_message(message, WRONG_USER_ID_MESSAGE)
            else:
                config.delete_admin_id(int(admin_to_delete))
                self.telegram_driver.answer_message(message, USER_DELETED_MESSAGE)

    def _do_delete_field(self, message):
        from_id = message["from_id"]
        if len(message["text"].split()) > 1:
            field_to_delete = message["text"].split()[1]
        else:
            self.telegram_driver.answer_message(message, DELETE_USER_ID_MESSAGE)
            field_to_delete = self.wait_for_answer(from_id)["text"]
        if not field_to_delete.isdigit() or int(field_to_delete) not in config.field_ids:
            self.telegram_driver.answer_message(message, WRONG_USER_ID_MESSAGE)
        else:
            config.delete_field_id(int(field_to_delete))
            self.telegram_driver.answer_message(message, USER_DELETED_MESSAGE)

    def _do_delete_kc(self, message):
        from_id = message["from_id"]
        if len(message["text"].split()) > 1:
            kc_to_delete = message["text"].split()[1]
        else:
            self.telegram_driver.answer_message(message, DELETE_USER_ID_MESSAGE)
            kc_to_delete = self.wait_for_answer(from_id)["text"]
        if not kc_to_delete.isdigit() or int(kc_to_delete) not in config.kc_ids:
            self.telegram_driver.answer_message(message, WRONG_USER_ID_MESSAGE)
        else:
            config.delete_kc_id(int(kc_to_delete))
            self.telegram_driver.answer_message(message, USER_DELETED_MESSAGE)

    def _do_edit_admin_pass(self, message):
        from_id = message["from_id"]
        if len(message["text"].split()) > 1:
            old = config.admin_passphrase
            new = message["text"].split()[1]
            if new not in config.passphrases:
                config.admin_passphrase = message["text"].split()[1]
                self.telegram_driver.answer_message(
                    message,
                    PASS_WAS_CHANGED.format(code1=old,
                                            code2=config.admin_passphrase))
            else:
                self.telegram_driver.answer_message(
                    message,
                    DUPLICATE_PASS)
        else:
            self.telegram_driver.answer_message(
                message,
                ENTER_NEW_PASS.format(code=config.admin_passphrase))
            old = config.admin_passphrase
            new = self.wait_for_answer(from_id)["text"]
            if new not in config.passphrases:
                config.admin_passphrase = new
                self.telegram_driver.answer_message(
                    message,
                    PASS_WAS_CHANGED.format(code1=old,
                                            code2=new))
            else:
                self.telegram_driver.answer_message(
                    message,
                    DUPLICATE_PASS)

    def _do_edit_field_pass(self, message):
        from_id = message["from_id"]
        if len(message["text"].split()) > 1:
            old = config.field_passphrase
            new = message["text"].split()[1]
            if new not in config.passphrases:
                config.field_passphrase = message["text"].split()[1]
                self.telegram_driver.answer_message(
                    message,
                    PASS_WAS_CHANGED.format(code1=old,
                                            code2=config.field_passphrase))
            else:
                self.telegram_driver.answer_message(
                    message,
                    DUPLICATE_PASS)
        else:
            self.telegram_driver.answer_message(
                message,
                ENTER_NEW_PASS.format(code=config.field_passphrase))
            old = config.field_passphrase
            new = self.wait_for_answer(from_id)["text"]
            if new not in config.passphrases:
                config.field_passphrase = new
                self.telegram_driver.answer_message(
                    message,
                    PASS_WAS_CHANGED.format(code1=old,
                                            code2=new))
            else:
                self.telegram_driver.answer_message(
                    message,
                    DUPLICATE_PASS)

    def _do_edit_kc_pass(self, message):
        from_id = message["from_id"]
        if len(message["text"].split()) > 1:
            old = config.kc_passphrase
            new = message["text"].split()[1]
            if new not in config.passphrases:
                config.kc_passphrase = message["text"].split()[1]
                self.telegram_driver.answer_message(
                    message,
                    PASS_WAS_CHANGED.format(code1=old,
                                            code2=config.kc_passphrase))
            else:
                self.telegram_driver.answer_message(
                    message,
                    DUPLICATE_PASS)
        else:
            self.telegram_driver.answer_message(
                message,
                ENTER_NEW_PASS.format(code=config.kc_passphrase))
            old = config.kc_passphrase
            new = self.wait_for_answer(from_id)["text"]
            if new not in config.passphrases:
                config.kc_passphrase = new
                self.telegram_driver.answer_message(
                    message,
                    PASS_WAS_CHANGED.format(code1=old,
                                            code2=new))
            else:
                self.telegram_driver.answer_message(
                    message,
                    DUPLICATE_PASS)

    def _do_disapprove(self, message):
        chat_id = message["chat_id"]
        self.telegram_driver.answer_message(message, AFFIRMATIVE_MESSAGES)
        self.group_chat_id = None
        self.paused = False
        self.telegram_driver.send_message(chat_id, DISAPPROVE_MESSAGES)

    def disapprove_command(self, message):
        from_id = message["from_id"]
        chat_id = message["chat_id"]
        if self._is_admin(from_id):
            if chat_id < 0:
                if chat_id == self.group_chat_id:
                    self._do_disapprove(message)
                else:
                    self.telegram_driver.answer_message(message, NO_GROUP_CHAT_MESSAGES)
            else:
                self.telegram_driver.answer_message(message, NOT_GROUP_CHAT_MESSAGES)
        elif config.answer_forbidden:
            self.telegram_driver.answer_message(message, ACCESS_VIOLATION_MESSAGES)

    def _do_status(self, message):
        hints_shown = ''
        for i in self.game_worker.hints_shown:
            hints_shown += str(i) + ' '
        status_message = STATUS_MESSAGE.format(
            paused=PAUSED_STATUS_MESSAGES[self.paused],
            chat_id=self.group_chat_id,
            game_connection=GAME_CONNECTION_MESSAGES[self.game_worker.game_driver.is_logged()],
            game_level_id=self.game_worker.last_level_shown,
            game_hint_id=hints_shown
        )
        self.telegram_driver.answer_message(message, status_message)

    def _do_info(self, message):
        info_message = INFO_MESSAGE.format(
            login=self.game_worker.game_driver.login,
            password=self.game_worker.game_driver.password,
            host=self.game_worker.game_driver.host,
            game_id=self.game_worker.game_driver.game_id,
            admins=json.dumps(self.get_usernames(config.admin_ids)),
            fields=json.dumps(self.get_usernames(config.field_ids)),
            kcs=json.dumps(self.get_usernames(config.kc_ids)),
            admin_passphrase=config.admin_passphrase,
            field_passphrase=config.field_passphrase,
            kc_passphrase=config.kc_passphrase)
        self.telegram_driver.answer_message(message, info_message)

    def _do_reset(self, message):
        self.game_worker.reset_level()
        self.telegram_driver.answer_message(message, BOT_WAS_RESET_MESSAGE)

    def _do_task(self, message):
        task_text = TASK_MESSAGE.format(
            level_number=self.game_worker.last_level_shown,
            task=self.game_worker.last_task_text)
        self.telegram_driver.answer_message(message, task_text, parse_mode="HTML")

    def _do_hints(self, message):
        hints = []
        for hint_id in sorted(self.game_worker.all_hints.keys()):
            hints.append(NEW_HINT_MESSAGE.format(
                smile=HINTS_APPEND,
                hint_number=hint_id,
                hint=self.game_worker.all_hints[hint_id]))
        for hint in hints:
            self.telegram_driver.answer_message(message, hint, parse_mode="HTML")

    def _do_help(self, message):
        from_id = message["from_id"]
        if self._is_admin(from_id):
            self.telegram_driver.answer_message(message, ADMIN_HELP_MESSAGE)
        else:
            self.telegram_driver.answer_message(message, REGULAR_HELP_MESSAGE)

    def _do_gap(self, message):
        codes_gap = self.game_worker.game_driver.get_codes_gap()
        self.telegram_driver.answer_message(message,
                                            codes_gap)

    def _do_edit_settings(self, message):
        from_id = message["from_id"]

        self.telegram_driver.send_message(
            from_id,
            GIVE_ME_LOGIN)
        GameDriver.login = self.wait_for_answer(from_id)["text"]
        config.game_login = GameDriver.login
        self.telegram_driver.send_message(
            from_id,
            GIVE_ME_PASSWORD)
        GameDriver.password = self.wait_for_answer(from_id)["text"]
        config.game_password = GameDriver.password
        self.telegram_driver.send_message(
            from_id,
            GIVE_ME_HOST)
        GameDriver.host = self.wait_for_answer(from_id)["text"]
        config.game_host = GameDriver.host
        self.telegram_driver.send_message(
            from_id,
            GIVE_ME_GAME)
        GameDriver.game_id = self.wait_for_answer(from_id)["text"]
        config.game_id = GameDriver.game_id

        self.game_worker = GameWorker()
        self.paused = True
        self.telegram_driver.admin_message(SETTINGS_WERE_CHANGED_MESSAGES)
        if self.game_worker.connected:
            self.telegram_driver.admin_message(CONNECTION_OK_MESSAGES)
            self.telegram_driver.admin_message(PLEASE_APPROVE_MESSAGES)
            self._do_reset(message)
            self.paused = False
            return True
        else:
            self.telegram_driver.admin_message(CONNECTION_PROBLEM_MESSAGES)
            self.telegram_driver.admin_message(CHECK_SETTINGS_MESSAGES)
            return False

    def _do_save_settings(self, message):
        result = config.save_config()
        if result:
            self.telegram_driver.answer_message(message, SETTINGS_WERE_SAVED_MESSAGES)
        else:
            self.telegram_driver.answer_message(message, SETTINGS_WERE_NOT_SAVED_MESSAGES)

    def unknown_command(self, message):
        if config.answer_unknown:
            self.telegram_driver.answer_message(message, UNKNOWN_MESSAGES)

    def process_messages(self):
        for message in self.check_new_messages():
            if self.initial_message is None:
                self.initial_message = message
            command = self.get_command(message)

            # User commands:
            if command in config.code_command:
                self.user_command(message, self._do_code)
            elif command in config.codes_command:
                self.user_command(message, self._do_codes)
            elif command == config.status_command:
                self.user_command(message, self._do_status)
            elif command == config.task_command:
                self.user_command(message, self._do_task)
            elif command == config.hints_command:
                self.user_command(message, self._do_hints)
            elif command == config.help_command:
                self.user_command(message, self._do_help)
            elif command == config.gap_command:
                self.user_command(message, self._do_gap)

            # Admin commands:
            elif command == config.approve_command:
                self.approve_command(message)
            elif command == config.disapprove_command:
                self.disapprove_command(message)
            elif command == config.stop_command:
                self.admin_command(message, self._do_stop)
            elif command == config.resume_command:
                self.admin_command(message, self._do_resume)
            elif command == config.pause_command:
                self.admin_command(message, self._do_pause)
            elif command == config.info_command:
                self.admin_command(message, self._do_info)
            elif command == config.reset_command:
                self.admin_command(message, self._do_reset)
            elif command == config.edit_command:
                self.admin_command(message, self._do_edit_settings)
            elif command == config.save_command:
                self.admin_command(message, self._do_save_settings)
            elif command == config.add_admin_command:
                self.admin_command(message, self._do_add_admin)
            elif command == config.delete_admin_command:
                self.admin_command(message, self._do_delete_admin)
            elif command == config.add_field_command:
                self.admin_command(message, self._do_add_field)
            elif command == config.delete_field_command:
                self.admin_command(message, self._do_delete_field)
            elif command == config.add_kc_command:
                self.admin_command(message, self._do_add_kc)
            elif command == config.delete_kc_command:
                self.admin_command(message, self._do_delete_kc)
            elif command == config.edit_admin_pass:
                self.admin_command(message, self._do_edit_admin_pass)
            elif command == config.edit_field_pass:
                self.admin_command(message, self._do_edit_field_pass)
            elif command == config.edit_kc_pass:
                self.admin_command(message, self._do_edit_kc_pass)
            else:
                self.unknown_command(message)

    def process_game_updates(self):
        if not self.paused and self.group_chat_id is not None:
            updates = self.game_worker.check_updates()
            if updates is None:
                self.telegram_driver.admin_message(CONNECTION_PROBLEM_MESSAGES)
            else:
                for update in updates:
                    self.telegram_driver.send_message(self.group_chat_id,
                                                      update,
                                                      parse_mode="HTML")
