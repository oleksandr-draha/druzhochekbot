# -*- coding: utf-8 -*-

import json
from random import choice

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
