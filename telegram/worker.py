# -*- coding: utf-8 -*-
import time
from random import choice

from game.driver import GameDriver
from game.worker import GameWorker
from telegram.dictionary import PAUSE_MESSAGES, GREETINGS_MESSAGES, LETS_GO_MESSAGES, START_PAUSE_MESSAGES, \
    RESUME_MESSAGES, END_PAUSE_MESSAGES, BYE_MESSAGES, NO_CODE_FOUND_MESSAGES, GIVE_ME_LOGIN, GIVE_ME_PASSWORD, \
    GIVE_ME_HOST, GIVE_ME_GAME, AFFIRMATIVE_MESSAGES, NOT_IN_CHAT_MESSAGES, CONNECTION_PROBLEM_MESSAGES, \
    CONNECTION_OK_MESSAGES, PLEASE_APPROVE_MESSAGES, TOO_MUCH_ATTEMPTS_MESSAGES, ACCESS_VIOLATION_MESSAGES
from telegram.driver import TelegramDriver


# TODO: To class attributes?
MAX_ATTEMPTS = 5
DRAGA_ID = 170302127
APPROVE_GROUP = '/approve'
CODE_COMMAND = '/c'
PAUSE_COMMAND = '/pause'
RESUME_COMMAND = '/resume'
STOP_COMMAND = '/stop'
HIGH_LEVEL_COMMANDS = [STOP_COMMAND, RESUME_COMMAND, APPROVE_GROUP]
IGNORE_COMMANDS = [PAUSE_COMMAND, CODE_COMMAND]


class TelegramWorker:
    initialize_attempts = 0

    def __init__(self):
        self.telegram_driver = TelegramDriver()
        self.telegram_driver.get_updates()
        self.initial_message = None
        self.paused = True
        self.stopped = False
        self.game_worker = None
        self.game_chat = None

        # Messages dictionary
        self.pause_messages = 0
        self.resume_messages = 0

    def setup_bot(self):
        messages = self.check_new_messages()
        if self.initialize_attempts == 0:
            self.telegram_driver.send_message(
                DRAGA_ID,
                "<b>-----------------------------------------</b>\r\n\r\n",
                parse_mode="HTML")
        if self.initialize_attempts >= MAX_ATTEMPTS:
            self.stopped = True
            self.telegram_driver.send_message(
                DRAGA_ID,
                TOO_MUCH_ATTEMPTS_MESSAGES)
            self.telegram_driver.send_message(
                DRAGA_ID,
                BYE_MESSAGES)
            return True

        for message in messages:
            message_text = message['message']['text']
            from_id = message['message']['from']['id']
            if message_text.startswith(STOP_COMMAND) and from_id == DRAGA_ID:
                self.stopped = True
                return True

        self.telegram_driver.send_message(
            DRAGA_ID,
            GREETINGS_MESSAGES)
        self.telegram_driver.send_message(
            DRAGA_ID,
            GIVE_ME_LOGIN)
        # GameDriver.login = self.wait_for_answer(DRAGA_ID)['message']['text']
        GameDriver.login = "druzhochek"
        self.telegram_driver.send_message(
            DRAGA_ID,
            GIVE_ME_PASSWORD)
        # GameDriver.password = self.wait_for_answer(DRAGA_ID)['message']['text']
        GameDriver.password = ""
        self.telegram_driver.send_message(
            DRAGA_ID,
            GIVE_ME_HOST)
        # GameDriver.game_id = self.wait_for_answer(DRAGA_ID)['message']['text']
        GameDriver.host = "online.quest.ua"
        self.telegram_driver.send_message(
            DRAGA_ID,
            GIVE_ME_GAME)
        # GameDriver.game_id = self.wait_for_answer(DRAGA_ID)['message']['text']
        GameDriver.game_id = "35727"
        self.telegram_driver.send_message(
            DRAGA_ID,
            choice(LETS_GO_MESSAGES))
        self.game_worker = GameWorker()
        if not self.game_worker.game_driver.is_logged():
            self.telegram_driver.send_message(
                DRAGA_ID,
                CONNECTION_PROBLEM_MESSAGES)
            self.initialize_attempts += 1
            return False
        else:
            self.telegram_driver.send_message(
                DRAGA_ID,
                CONNECTION_OK_MESSAGES)
            self.telegram_driver.send_message(
                DRAGA_ID,
                PLEASE_APPROVE_MESSAGES)
            self.initialize_attempts = 0
            return True


    @staticmethod
    def check_answer_from_chat_id(chat_id, messages):
        for message in messages:
            if message['message']['from']['id'] == chat_id \
                    and 'text' in message['message']:
                return message

    def wait_for_answer(self, chat_id):
        answer = self.check_answer_from_chat_id(DRAGA_ID,
                                                self.check_new_messages())
        while answer is None:
            answer = self.check_answer_from_chat_id(DRAGA_ID,
                                                    self.check_new_messages())
            time.sleep(1)
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

    def check_codes(self, message):
        codes = message['message']['text'].replace(CODE_COMMAND, '').rstrip().lstrip()
        codes = codes.split()
        results = choice(NO_CODE_FOUND_MESSAGES)
        if len(codes):
            results = ''
            for code in codes:
                result = self.game_worker.game_driver.try_code(code)
                if result:
                    results += '\r\n{code}: +'.format(code=code)
                else:
                    results += '\r\n{code}: Неверный код!!!'.format(code=code)
        return results

    def process_messages(self):
        for message in self.check_new_messages():
            if self.initial_message is None:
                self.initial_message = message
            message_text = message['message']['text']
            from_id = message['message']['from']['id']
            chat_id = message['message']['chat']['id']

            # TODO: To parsers and return command, arguments, function
            # region APPROVE GROUP COMMAND
            if message_text.startswith(APPROVE_GROUP):
                if from_id == DRAGA_ID:
                    if chat_id < 0:
                        self.telegram_driver.answer_message(
                            message,
                            AFFIRMATIVE_MESSAGES)
                        self.game_chat = chat_id
                        self.paused = False
                        self.telegram_driver.send_message(
                            self.game_chat,
                            LETS_GO_MESSAGES)
                    else:
                        self.telegram_driver.answer_message(
                            message,
                            NOT_IN_CHAT_MESSAGES)
                else:
                    self.telegram_driver.answer_message(
                        message,
                        ACCESS_VIOLATION_MESSAGES)
            # endregion

            # region STOP COMMAND
            if message_text.startswith(STOP_COMMAND):
                if from_id == DRAGA_ID:
                    self.telegram_driver.answer_message(
                        message,
                        BYE_MESSAGES)
                    self.stopped = True
                else:
                    self.telegram_driver.answer_message(
                        message,
                        ACCESS_VIOLATION_MESSAGES)
            # endregion

            # region PAUSE COMMAND
            if message_text.startswith(PAUSE_COMMAND):
                if from_id == DRAGA_ID:
                    if not self.paused:
                        self.pause_messages = 0
                        self.telegram_driver.answer_message(
                            message,
                            START_PAUSE_MESSAGES)
                        self.paused = True
                    else:
                        self.pause_messages += 1
                        pause_message = PAUSE_MESSAGES[self.pause_messages - 1] \
                            if len(PAUSE_MESSAGES) > self.pause_messages \
                            else PAUSE_MESSAGES[-1]
                        self.telegram_driver.answer_message(message, pause_message)
                else:
                    self.telegram_driver.answer_message(
                        message,
                        ACCESS_VIOLATION_MESSAGES)
            # endregion

            # region RESUME COMMAND
            if message_text.startswith(RESUME_COMMAND):
                if from_id == DRAGA_ID:
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
                else:
                    self.telegram_driver.answer_message(
                        message,
                        ACCESS_VIOLATION_MESSAGES)
            # endregion

            # region CODE COMMAND
            if message_text.startswith(CODE_COMMAND) and chat_id == self.game_chat:
                if not self.paused:
                    result = self.check_codes(message)
                    self.telegram_driver.answer_message(message, result)
                else:
                    self.pause_messages += 1
                    pause_message = PAUSE_MESSAGES[self.pause_messages - 1] \
                        if len(PAUSE_MESSAGES) > self.pause_messages \
                        else PAUSE_MESSAGES[-1]
                    self.telegram_driver.answer_message(message, pause_message)
                    # endregion

    def process_game_tasks(self):
        if not self.paused:
            updates = self.game_worker.check_updates()
            if len(updates) and self.game_chat is not None:
                for update in updates:
                    self.telegram_driver.send_message(self.game_chat,
                                                      update,
                                                      parse_mode="HTML")
            elif updates is None:
                self.telegram_driver.send_message(
                    DRAGA_ID,
                    CONNECTION_PROBLEM_MESSAGES)
