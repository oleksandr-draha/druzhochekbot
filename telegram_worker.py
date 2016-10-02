# -*- coding: utf-8 -*-
import time

from game_driver import GameDriver
from game_worker import GameWorker
from telegram_driver import TelegramDriver

MAX_ATTEMPTS = 5

DRAGA_ID = 170302127
CODE_COMMAND = '/c'


class TelegramWorker:

    def __init__(self):
        self.telegram_driver = TelegramDriver()
        self.initial_message = None
        self.setup_bot()
        self.game_worker = GameWorker()

    def setup_bot(self):
        self.check_new_messages()
        self.telegram_driver.send_message(
            DRAGA_ID,
            u"Привет! Я твой дружочек. Соскучился? "
            u"А я да. Давай мне свой логин для игры.")
        GameDriver.login = self.wait_for_answer(DRAGA_ID)['message']['text']
        self.telegram_driver.send_message(
            DRAGA_ID,
            u"Ага, ага. А пароль?")
        GameDriver.password = self.wait_for_answer(DRAGA_ID)['message']['text']
        self.telegram_driver.send_message(
            DRAGA_ID,
            u"Ок, какая игра?")
        GameDriver.game_id = self.wait_for_answer(DRAGA_ID)['message']['text']
        self.telegram_driver.send_message(
            DRAGA_ID,
            u"Ну всё, погнали!")

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

    def process_messages(self):
        for message in self.check_new_messages():
            if self.initial_message is None:
                self.initial_message = message
            if message['message']['text'].startswith(CODE_COMMAND):
                codes = message['message']['text'].replace(CODE_COMMAND, '').rstrip().lstrip()
                codes = codes.split()
                if len(codes):
                    results = ''
                    for code in codes:
                        result = self.game_worker.game_driver.try_code(code)
                        if result:
                            results += '\r\n{code}: +'.format(code=code)
                        else:
                            results += '\r\n{code}: INCORRECT!!!'.format(code=code)
                    self.telegram_driver.answer_message(message, results)
        update = self.game_worker.check_updates()
        if update is not None and self.initial_message is not None:
            self.telegram_driver.answer_message(self.initial_message, update)
        time.sleep(1)