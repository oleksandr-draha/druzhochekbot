import json
from random import choice

import requests

# TODO: To class attributes?
URL_UPDATES = "https://api.telegram.org/bot{key}/getUpdates?offset={offset}"
URL_SEND_MESSAGE = "https://api.telegram.org/bot{key}/sendMessage"
API_KEY = file("default.yaml").read()


class TelegramDriver():
    start_offset = 0
    session = None

    def __init__(self):
        if self.session is None:
            self.session = requests.session()

    def get_updates(self):
        r = self.session.get(URL_UPDATES.format(key=API_KEY, offset=self.start_offset))
        messages = json.loads(r.content)['result']
        income_message_count = len(messages)
        self.start_offset = messages[income_message_count - 1]['update_id'] + 1 \
            if income_message_count else 0
        return messages

    def send_message(self, chat_id, text, parse_mode="Markdown"):
        if isinstance(text, list):
            text_message = choice(text)
        else:
            text_message = text
        response = {"chat_id": chat_id,
                    "text": text_message,
                    "parse_mode": parse_mode}
        self.session.post(URL_SEND_MESSAGE.format(key=API_KEY),
                      params=response)

    def answer_message(self, message, text):
        self.send_message(message['message']['chat']['id'], text)
