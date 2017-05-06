# -*- coding: utf-8 -*-

import json
from random import choice

import time
from requests import ConnectionError, session

from config.config import config


class TelegramDriver:
    def __init__(self):
        self.start_offset = 0
        self.session = session()

    def get_updates(self):
        try:
            r = self.session.get(
                config.updates_path.format(key=config.bot_token,
                                           offset=self.start_offset))
            messages = json.loads(r.content)['result']
            income_message_count = len(messages)
            # Use in order to get smile code
            # send /c_+ smile
            # ord(messages[0]["message"]["text"][3])
            # ord(messages[0]["message"]["text"][4])
            self.start_offset = messages[income_message_count - 1]['update_id'] + 1 \
                if income_message_count else 0
            return messages
        except ConnectionError:
            return {}

    def get_username(self, user_id):
        try:
            r = self.session.get(
                config.users_path.format(key=config.bot_token,
                                         user_id=user_id))
            return json.loads(r.content).get('result', {}).get('username')
        except ConnectionError:
            return {}

    def send_message(self, chat_id, text, parse_mode="Markdown", reply_to=None):
        if isinstance(text, list):
            text_message = choice(text)
        else:
            text_message = text
        response = {"chat_id": chat_id,
                    "text": text_message,
                    "parse_mode": parse_mode}
        if reply_to is not None:
            response.update({"reply_to_message_id": reply_to})
        try:
            self.session.post(
                config.send_message_path.format(key=config.bot_token),
                params=response)
        except ConnectionError:
            return

    def answer_message(self, message, text, parse_mode="Markdown"):
        self.send_message(message["chat_id"],
                          text,
                          reply_to=message["id"],
                          parse_mode=parse_mode)

    def admin_message(self, text):
        for admin_id in config.admin_ids:
            self.send_message(admin_id, text)

    def get_usernames(self, users):
        usernames = {}
        for user in users:
            usernames.setdefault(user, self.get_username(user))
        return usernames

    def check_new_messages(self):
        """
        Checks whether new text messages present in the channel
        :return:
        :rtype: list of dict
        """
        messages = []
        for message in self.get_updates():
            if message.get('message', {}).get('text') is not None:
                messages.append(
                    {'id': message.get('message', {}).get('message_id'),
                     'text': message.get('message', {}).get('text'),
                     'from_id': message.get('message', {}).get('from', {}).get('id'),
                     'chat_id': message.get('message', {}).get('chat', {}).get('id')})
        return messages

    @staticmethod
    def is_user(from_id):
        return from_id in config.admin_ids + config.field_ids + config.field_ids

    @staticmethod
    def is_admin(from_id):
        return from_id in config.admin_ids

    @staticmethod
    def is_field(from_id):
        return from_id in config.field_ids

    @staticmethod
    def is_kc(from_id):
        return from_id in config.kc_ids

    @staticmethod
    def get_command(message):
        if message["text"].startswith('/'):
            return message["text"].split()[0].split('@')[0]
        else:
            return ''

    @staticmethod
    def get_message_text(message):
        if TelegramDriver.get_command(message) is not None:
            return message["text"].replace(TelegramDriver.get_command(message), '').lstrip()
        else:
            return message["text"]

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
