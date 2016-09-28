# -*- coding: utf-8 -*-
import json
import requests
import time

start_offset = 0
initialized = False
URL_UPDATES = "https://api.telegram.org/bot{key}/getUpdates?offset={offset}"
URL_SEND_MESSAGE = "https://api.telegram.org/bot{key}/sendMessage"
API_KEY = file("default.yaml").read()

VERY_FUNNY_ANSWERS = {u"ет": u"коммуниста ответ",
                      u"иста": u"сам знаешь что у тракториста"}

while True:
    r = requests.get(URL_UPDATES.format(key=API_KEY, offset=start_offset))
    messages_raw = json.loads(r.content)
    income_message_count = len(messages_raw['result'])
    if initialized and income_message_count:
        # TODO: some actions on messages
        start_offset = messages_raw['result'][income_message_count - 1]['update_id'] + 1
        messages = messages_raw['result']
        for message in messages:
            original_message = message["message"]["text"].lower()
            answer = u"Чёт с рифмой никак"
            for line in VERY_FUNNY_ANSWERS:
                if original_message.endswith(line):
                    answer = VERY_FUNNY_ANSWERS[line]
            response = {"chat_id": message["message"]["chat"]["id"],
                        "text": answer}
            requests.post(URL_SEND_MESSAGE.format(key=API_KEY),
                          params=response)
    if not initialized and income_message_count:
        start_offset = messages_raw['result'][income_message_count - 1]['update_id'] + 1
        initialized = True
    time.sleep(1)