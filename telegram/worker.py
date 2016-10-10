# -*- coding: utf-8 -*-
import time

from config.config import config
from config.dictionary import PAUSED_MESSAGES, LETS_GO_MESSAGES, START_PAUSE_MESSAGES, \
    RESUME_MESSAGES, END_PAUSE_MESSAGES, BYE_MESSAGES, NO_CODE_FOUND_MESSAGE, GIVE_ME_LOGIN, GIVE_ME_PASSWORD, \
    GIVE_ME_HOST, GIVE_ME_GAME, AFFIRMATIVE_MESSAGES, NOT_GROUP_CHAT_MESSAGES, CONNECTION_PROBLEM_MESSAGES, \
    CONNECTION_OK_MESSAGES, PLEASE_APPROVE_MESSAGES, ACCESS_VIOLATION_MESSAGES, \
    ALREADY_PAUSED_MESSAGES, UNKNOWN_MESSAGES, WRONG_CODE_MESSAGE, STATUS_MESSAGE, \
    PAUSED_STATUS_MESSAGES, GAME_CONNECTION_MESSAGES, INFO_MESSAGE, NOT_FOR_GROUP_CHAT_MESSAGES, NO_GROUP_CHAT_MESSAGES, \
    DISAPPROVE_MESSAGES, BOT_WAS_RESET_MESSAGE, HELP_MESSAGE, CHECK_SETTINGS_MESSAGES, SETTINGS_WERE_CHANGED_MESSAGES, \
    SETTINGS_WERE_SAVED_MESSAGES, SETTINGS_WERE_NOT_SAVED_MESSAGES
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

        # Messages dictionary
        self.pause_messages = 0
        self.resume_messages = 0

        self.load_settings()

    @staticmethod
    def _is_admin(from_id):
        return from_id in config.admin_ids

    def load_settings(self):
        GameDriver.login = config.game_login
        GameDriver.password = config.game_password
        GameDriver.game_id = config.game_id
        GameDriver.host = config.game_host
        self.game_worker = GameWorker()
        if self.game_worker.connected:
            self.telegram_driver.admin_message(
                CONNECTION_OK_MESSAGES)
            self.telegram_driver.admin_message(
                PLEASE_APPROVE_MESSAGES)
            return True
        else:
            self.telegram_driver.admin_message(
                CONNECTION_PROBLEM_MESSAGES)
            self.telegram_driver.admin_message(
                CHECK_SETTINGS_MESSAGES)
            # TODO: add check settings message
            return False

    @staticmethod
    def check_answer_from_chat_id(chat_id, messages):
        for message in messages:
            if message['message']['from']['id'] == chat_id \
                    and 'text' in message['message']:
                return message

    def wait_for_answer(self, from_id):
        answer = None
        while answer is None:
            answer = self.check_answer_from_chat_id(from_id,
                                                    self.check_new_messages())
            time.sleep(config.answer_check_interval)
        return answer

    def check_new_messages(self):
        """
        :return:
        :rtype: list of dict
        """
        messages_with_text = []
        messages = self.telegram_driver.get_updates()
        for message in messages:
            if 'message' in message and 'text' in message['message']:
                messages_with_text.append(message)
        return messages_with_text

    def check_codes(self, message, command):
        codes = message['message']['text'].replace(command, '').rstrip().lstrip()
        codes = codes.split()
        results = NO_CODE_FOUND_MESSAGE
        if len(codes):
            results = ''
            for code in codes:
                result = self.game_worker.game_driver.try_code(code)
                if result:
                    results += u'\r\n{code}: +'.format(code=code)
                else:
                    results += u'\r\n{code}: {wrong}'.format(code=code,
                                                             wrong=WRONG_CODE_MESSAGE)
        return results

    def check_code(self, message, command):
        code = message['message']['text'].replace(command, '').rstrip().lstrip()
        results = NO_CODE_FOUND_MESSAGE
        if len(code):
            result = self.game_worker.game_driver.try_code(code)
            if result:
                results = u'\r\n{code}: +'.format(code=code)
            else:
                results = u'\r\n{code}: {wrong}'.format(code=code,
                                                        wrong=WRONG_CODE_MESSAGE)
        return results

    @staticmethod
    def get_command(message):
        return message.split()[0]

    def _do_stop(self, message):
        self.telegram_driver.answer_message(
            message,
            BYE_MESSAGES)
        self.stopped = True

    def stop_command(self, message):
        from_id = message['message']['from']['id']
        chat_id = message['message']['chat']['id']
        if self._is_admin(from_id):
            if chat_id < 0:
                if chat_id == self.group_chat_id:
                    self._do_stop(message)
                else:
                    self.telegram_driver.answer_message(
                        message,
                        NOT_FOR_GROUP_CHAT_MESSAGES)
            else:
                self._do_stop(message)
        else:
            self.telegram_driver.answer_message(
                message,
                ACCESS_VIOLATION_MESSAGES)

    def _do_pause(self, message):
        if not self.paused:
            self.pause_messages = 0
            self.telegram_driver.answer_message(
                message,
                START_PAUSE_MESSAGES)
            self.paused = True
        else:
            self.pause_messages += 1
            pause_message = ALREADY_PAUSED_MESSAGES[self.pause_messages - 1] \
                if len(ALREADY_PAUSED_MESSAGES) > self.pause_messages \
                else ALREADY_PAUSED_MESSAGES[-1]
            self.telegram_driver.answer_message(message, pause_message)

    def pause_command(self, message):
        from_id = message['message']['from']['id']
        chat_id = message['message']['chat']['id']
        if self._is_admin(from_id):
            if chat_id < 0:
                if chat_id == self.group_chat_id:
                    self._do_pause(message)
                else:
                    self.telegram_driver.answer_message(
                        message,
                        NOT_FOR_GROUP_CHAT_MESSAGES)
            else:
                self._do_pause(message)
        else:
            self.telegram_driver.answer_message(
                message,
                ACCESS_VIOLATION_MESSAGES)

    def _do_resume(self, message):
        if self.paused:
            self.resume_messages = 0
            self.telegram_driver.answer_message(
                message,
                END_PAUSE_MESSAGES)
            self.paused = False
        else:
            self.resume_messages += 1
            resume_message = RESUME_MESSAGES[self.resume_messages - 1] \
                if len(RESUME_MESSAGES) > self.resume_messages \
                else RESUME_MESSAGES[-1]
            self.telegram_driver.answer_message(message, resume_message)

    def resume_command(self, message):
        from_id = message['message']['from']['id']
        chat_id = message['message']['chat']['id']
        if self._is_admin(from_id):
            if chat_id < 0:
                if chat_id == self.group_chat_id:
                    self._do_resume(message)
                else:
                    self.telegram_driver.answer_message(
                        message,
                        NOT_FOR_GROUP_CHAT_MESSAGES)
            else:
                self._do_resume(message)
        else:
            self.telegram_driver.answer_message(
                message,
                ACCESS_VIOLATION_MESSAGES)

    def _do_codes(self, message, command):
        if not self.paused:
            result = self.check_codes(message, command)
            self.telegram_driver.answer_message(message, result)
        else:
            self.pause_messages += 1
            pause_message = PAUSED_MESSAGES[self.pause_messages - 1] \
                if len(PAUSED_MESSAGES) > self.pause_messages \
                else PAUSED_MESSAGES[-1]
            self.telegram_driver.answer_message(message, pause_message)

    def codes_command(self, message, command):
        from_id = message['message']['from']['id']
        chat_id = message['message']['chat']['id']
        if chat_id < 0:
            if chat_id == self.group_chat_id:
                self._do_codes(message, command)
            elif self._is_admin(from_id):
                self.telegram_driver.answer_message(
                    message,
                    NOT_GROUP_CHAT_MESSAGES)
            else:
                self.telegram_driver.answer_message(
                    message,
                    ACCESS_VIOLATION_MESSAGES)
        elif self._is_admin(from_id):
            self._do_codes(message, command)
        else:
            self.telegram_driver.answer_message(
                message,
                ACCESS_VIOLATION_MESSAGES)

    def _do_code(self, message, command):
        if not self.paused:
            result = self.check_code(message, command)
            self.telegram_driver.answer_message(message, result)
        else:
            self.pause_messages += 1
            pause_message = PAUSED_MESSAGES[self.pause_messages - 1] \
                if len(PAUSED_MESSAGES) > self.pause_messages \
                else PAUSED_MESSAGES[-1]
            self.telegram_driver.answer_message(message, pause_message)

    def code_command(self, message, command):
        from_id = message['message']['from']['id']
        chat_id = message['message']['chat']['id']
        if chat_id < 0:
            if chat_id == self.group_chat_id:
                self._do_code(message, command)
            elif self._is_admin(from_id):
                self.telegram_driver.answer_message(
                    message,
                    NO_GROUP_CHAT_MESSAGES)
            else:
                self.telegram_driver.answer_message(
                    message,
                    ACCESS_VIOLATION_MESSAGES)
        elif self._is_admin(from_id):
            self._do_code(message, command)
        else:
            self.telegram_driver.answer_message(
                message,
                ACCESS_VIOLATION_MESSAGES)

    def _do_approve(self, message):
        chat_id = message['message']['chat']['id']
        self.telegram_driver.answer_message(
            message,
            AFFIRMATIVE_MESSAGES)
        self.group_chat_id = chat_id
        self.paused = False
        self.telegram_driver.send_message(
            self.group_chat_id,
            LETS_GO_MESSAGES)

    def approve_command(self, message):
        from_id = message['message']['from']['id']
        chat_id = message['message']['chat']['id']
        if self._is_admin(from_id):
            if chat_id < 0:
                self._do_approve(message)
            else:
                self.telegram_driver.answer_message(
                    message,
                    NOT_GROUP_CHAT_MESSAGES)
        else:
            self.telegram_driver.answer_message(
                message,
                ACCESS_VIOLATION_MESSAGES)

    def _do_disapprove(self, message):
        chat_id = message['message']['chat']['id']
        self.telegram_driver.answer_message(
            message,
            AFFIRMATIVE_MESSAGES)
        self.group_chat_id = None
        self.paused = False
        self.telegram_driver.send_message(
            chat_id,
            DISAPPROVE_MESSAGES)

    def disapprove_command(self, message):
        from_id = message['message']['from']['id']
        chat_id = message['message']['chat']['id']
        if self._is_admin(from_id):
            if chat_id < 0:
                if chat_id == self.group_chat_id:
                    self._do_disapprove(message)
                else:
                    self.telegram_driver.answer_message(
                        message,
                        NO_GROUP_CHAT_MESSAGES)
            else:
                self.telegram_driver.answer_message(
                    message,
                    NOT_GROUP_CHAT_MESSAGES)
        else:
            self.telegram_driver.answer_message(
                message,
                ACCESS_VIOLATION_MESSAGES)

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
        self.telegram_driver.answer_message(message,
                                            status_message)

    def status_command(self, message):
        from_id = message['message']['from']['id']
        chat_id = message['message']['chat']['id']
        if chat_id < 0:
            if chat_id == self.group_chat_id:
                self._do_status(message)
            elif self._is_admin(from_id):
                self.telegram_driver.answer_message(
                    message,
                    NO_GROUP_CHAT_MESSAGES)
            else:
                self.telegram_driver.answer_message(
                    message,
                    ACCESS_VIOLATION_MESSAGES)
        elif self._is_admin(from_id):
            self._do_status(message)
        else:
            self.telegram_driver.answer_message(
                message,
                ACCESS_VIOLATION_MESSAGES)

    def _do_info(self, message):
        info_message = INFO_MESSAGE.format(
            login=self.game_worker.game_driver.login,
            password=self.game_worker.game_driver.password,
            host=self.game_worker.game_driver.host,
            game_id=self.game_worker.game_driver.game_id)
        self.telegram_driver.answer_message(message,
                                            info_message)

    def info_command(self, message):
        from_id = message['message']['from']['id']
        chat_id = message['message']['chat']['id']
        if self._is_admin(from_id):
            if chat_id < 0:
                self.telegram_driver.answer_message(
                    message,
                    NOT_FOR_GROUP_CHAT_MESSAGES)
            else:
                self._do_info(message)
        else:
            self.telegram_driver.answer_message(
                message,
                ACCESS_VIOLATION_MESSAGES)

    def _do_reset(self, message):
        self.game_worker.reset()
        self.telegram_driver.answer_message(message, BOT_WAS_RESET_MESSAGE)

    def reset_command(self, message):
        from_id = message['message']['from']['id']
        chat_id = message['message']['chat']['id']
        if chat_id < 0:
            if self._is_admin(from_id):
                if chat_id == self.group_chat_id:
                    self._do_reset(message)
                else:
                    self.telegram_driver.answer_message(
                        message,
                        NO_GROUP_CHAT_MESSAGES)
            else:
                self.telegram_driver.answer_message(
                    message,
                    ACCESS_VIOLATION_MESSAGES)
        elif self._is_admin(from_id):
            self._do_reset(message)
        else:
            self.telegram_driver.answer_message(
                message,
                ACCESS_VIOLATION_MESSAGES)

    def _do_task(self):
        self.game_worker.last_level_shown = None
        self.game_worker.finished_shown = False

    def task_command(self, message):
        from_id = message['message']['from']['id']
        chat_id = message['message']['chat']['id']
        if chat_id < 0:
            if chat_id == self.group_chat_id:
                self._do_task()
            elif self._is_admin(from_id):
                self.telegram_driver.answer_message(
                    message,
                    NO_GROUP_CHAT_MESSAGES)
            else:
                self.telegram_driver.answer_message(
                    message,
                    ACCESS_VIOLATION_MESSAGES)
        elif self._is_admin(from_id):
            self._do_task()
        else:
            self.telegram_driver.answer_message(
                message,
                ACCESS_VIOLATION_MESSAGES)

    def _do_hints(self):
        self.game_worker.hints_shown = []

    def hints_command(self, message):
        from_id = message['message']['from']['id']
        chat_id = message['message']['chat']['id']
        if chat_id < 0:
            if chat_id == self.group_chat_id:
                self._do_hints()
            elif self._is_admin(from_id):
                self.telegram_driver.answer_message(
                    message,
                    NO_GROUP_CHAT_MESSAGES)
            else:
                self.telegram_driver.answer_message(
                    message,
                    ACCESS_VIOLATION_MESSAGES)
        elif self._is_admin(from_id):
            self._do_hints()
        else:
            self.telegram_driver.answer_message(
                message,
                ACCESS_VIOLATION_MESSAGES)

    def _do_help(self, message):
        self.telegram_driver.answer_message(
            message,
            HELP_MESSAGE)

    def help_command(self, message):
        from_id = message['message']['from']['id']
        chat_id = message['message']['chat']['id']
        if chat_id < 0:
            if chat_id == self.group_chat_id:
                self._do_help(message)
            elif self._is_admin(from_id):
                self.telegram_driver.answer_message(
                    message,
                    NO_GROUP_CHAT_MESSAGES)
            else:
                self.telegram_driver.answer_message(
                    message,
                    ACCESS_VIOLATION_MESSAGES)
        elif self._is_admin(from_id):
            self._do_help(message)
        else:
            self.telegram_driver.answer_message(
                message,
                ACCESS_VIOLATION_MESSAGES)

    def _do_edit_settings(self, message):
        from_id = message['message']['from']['id']

        self.telegram_driver.send_message(
            from_id,
            GIVE_ME_LOGIN)
        GameDriver.login = self.wait_for_answer(from_id)['message']['text']
        config.game_login = GameDriver.login
        self.telegram_driver.send_message(
            from_id,
            GIVE_ME_PASSWORD)
        GameDriver.password = self.wait_for_answer(from_id)['message']['text']
        config.game_password = GameDriver.password
        self.telegram_driver.send_message(
            from_id,
            GIVE_ME_HOST)
        GameDriver.host = self.wait_for_answer(from_id)['message']['text']
        config.game_host = GameDriver.host
        self.telegram_driver.send_message(
            from_id,
            GIVE_ME_GAME)
        GameDriver.game_id = self.wait_for_answer(from_id)['message']['text']
        config.game_id = GameDriver.game_id

        self.game_worker = GameWorker()
        self.paused = True
        self.telegram_driver.admin_message(
            SETTINGS_WERE_CHANGED_MESSAGES)
        if self.game_worker.connected:
            self.telegram_driver.admin_message(
                CONNECTION_OK_MESSAGES)
            self.telegram_driver.admin_message(
                PLEASE_APPROVE_MESSAGES)
            self._do_reset()
            self.paused = False
            return True
        else:
            self.telegram_driver.admin_message(
                CONNECTION_PROBLEM_MESSAGES)
            self.telegram_driver.admin_message(
                CHECK_SETTINGS_MESSAGES)
            return False

    def edit_settings_command(self, message):
        from_id = message['message']['from']['id']
        chat_id = message['message']['chat']['id']
        if self._is_admin(from_id):
            if chat_id < 0:
                if chat_id == self.group_chat_id:
                    self.telegram_driver.answer_message(
                        message,
                        NOT_FOR_GROUP_CHAT_MESSAGES)
                else:
                    self.telegram_driver.answer_message(
                        message,
                        NO_GROUP_CHAT_MESSAGES)
            else:
                self._do_edit_settings(message)
        else:
            self.telegram_driver.answer_message(
                message,
                ACCESS_VIOLATION_MESSAGES)

    def _do_save_settings(self, message):
        result = config.save_config()
        if result:
            self.telegram_driver.answer_message(
                message,
                SETTINGS_WERE_SAVED_MESSAGES)
        else:
            self.telegram_driver.answer_message(
                message,
                SETTINGS_WERE_NOT_SAVED_MESSAGES)

    def save_settings_command(self, message):
        from_id = message['message']['from']['id']
        chat_id = message['message']['chat']['id']
        if self._is_admin(from_id):
            if chat_id < 0:
                if chat_id == self.group_chat_id:
                    self.telegram_driver.answer_message(
                        message,
                        NOT_FOR_GROUP_CHAT_MESSAGES)
                else:
                    self.telegram_driver.answer_message(
                        message,
                        NO_GROUP_CHAT_MESSAGES)
            else:
                self._do_save_settings(message)
        else:
            self.telegram_driver.answer_message(
                message,
                ACCESS_VIOLATION_MESSAGES)

    def _do_unknown(self, message):
        self.telegram_driver.answer_message(
            message,
            UNKNOWN_MESSAGES)

    def unknown_command(self, message):
        if config.answer_unknown:
            self.telegram_driver.answer_message(message,
                                                UNKNOWN_MESSAGES)

    def process_messages(self):
        for message in self.check_new_messages():
            if self.initial_message is None:
                self.initial_message = message
            message_text = message['message']['text']
            command = self.get_command(message_text)

            if command in config.code_command:
                self.code_command(message, command)
            elif command in config.codes_command:
                self.codes_command(message, command)
            elif command == config.stop_command:
                self.stop_command(message)
            elif command == config.resume_command:
                self.resume_command(message)
            elif command == config.pause_command:
                self.pause_command(message)
            elif command == config.approve_command:
                self.approve_command(message)
            elif command == config.disapprove_command:
                self.disapprove_command(message)
            elif command == config.status_command:
                self.status_command(message)
            elif command == config.info_command:
                self.info_command(message)
            elif command == config.edit_command:
                self.edit_settings_command(message)
            elif command == config.save_command:
                self.save_settings_command(message)
            elif command == config.reset_command:
                self.reset_command(message)
            elif command == config.task_command:
                self.task_command(message)
            elif command == config.hints_command:
                self.hints_command(message)
            elif command.startswith(config.help_command):
                self.help_command(message)
            # TODO: add adding admins
            # NTI1MjkyNzc=
            # Step 1 - add admin
            # Step 2 - select password
            # Step 3 - wait for some account to send this password and
            # add it to admins list
            # Removing admin - ???
            else:
                self.unknown_command(message)

    def process_game_updates(self):
        if not self.paused and self.group_chat_id is not None:
            updates = self.game_worker.check_updates()
            if updates is None:
                self.telegram_driver.admin_message(
                    CONNECTION_PROBLEM_MESSAGES)
            elif len(updates):
                for update in updates:
                    self.telegram_driver.send_message(self.group_chat_id,
                                                      update,
                                                      parse_mode="HTML"
                                                      )
