# -*- coding: utf-8 -*-
import json
from random import choice
import time

from requests import ConnectionError, ReadTimeout, session

from config import bot_settings, timeouts
from config.dictionary import SettingsMessages


class TelegramDriver(object):
    def __init__(self):
        self.start_offset = 0
        self.session = session()
        self.get_updates()

    def get_updates(self):
        """
        Perform request to Telegram server in order to receive new messages,
        addressed to bot.
        :return: list of messages
        :rtype: list
        """
        try:
            r = self.session.get(
                bot_settings.updates_path.format(key=bot_settings.bot_token,
                                                 offset=self.start_offset))
            messages = json.loads(r.content)['result']
            # Use in order to get smile code
            # send /c_+ smile
            # ord(messages[0]["message"]["text"][3])
            if len(messages):
                self.start_offset = messages[-1]['update_id'] + 1
            # ord(messages[0]["message"]["text"][4])
            return messages
        except (ConnectionError, ReadTimeout):
            return {}

    def get_username(self, user_id):
        """
        Perform request to Telegram API and extract username by given user_id if possible
        :param user_id:
        :type user_id: int
        :return: username
        :rtype: str or None
        """
        try:
            r = self.session.get(
                bot_settings.users_path.format(key=bot_settings.bot_token,
                                               user_id=user_id))
            return json.loads(r.content).get('result', {}).get('username')
        except ConnectionError:
            return {}

    def get_usernames(self, users):
        """
        Return list of usernames for specified user ids
        :type users: list of int
        :rtype: dict
        """
        usernames = {}
        for user in users:
            usernames.setdefault(user, self.get_username(user))
        return usernames

    def send_message(self, chat_id, text, reply_to=None, parse_mode="Markdown"):
        """
        Send message to specified chat_id. If reply_to is specified - it will be an answer
        for message_id
        :type chat_id: int
        :type text: str or unicode
        :type reply_to: int
        :type parse_mode: str
        :rtype: None
        """
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
                bot_settings.send_message_path.format(key=bot_settings.bot_token),
                params=response)
        except ConnectionError:
            return

    def send_file(self, chat_id, document, name, caption="Requested data"):
        """
        Send file to specified chat_id. File is made from document string.
        :type chat_id: int
        :type document: str or unicode
        :param name: File name
        :type name: str
        :param caption: Caption will be shown in chat message
        :rtype: None
        """
        files = {'document': (name, document)}
        response = {"chat_id": chat_id,
                    "document": None,
                    "caption": caption}
        try:
            self.session.post(
                bot_settings.send_document_path.format(key=bot_settings.bot_token),
                params=response,
                files=files)
        except ConnectionError:
            return

    def get_file(self, file_id):
        """
        Get a file info (used to receive photos, sent in group chat)
        :param file_id: original file_id
        :rtype: file
        """
        try:
            r = self.session.get(
                bot_settings.get_file_path.format(key=bot_settings.bot_token, file_id=file_id))
            file_path = json.loads(r.content).get("result", {}).get("file_path")
            if file_path is not None:
                download_link = bot_settings.download_file_path.format(key=bot_settings.bot_token, file_id=file_path)
                return download_link
        except ConnectionError:
            return

    def answer_message(self, message, text, parse_mode="Markdown"):
        """
        Send message as an answer to the specified message
        :param message: original message
        :type message: dict
        :type text: str or unicode
        :type parse_mode: str
        :rtype: None
        """
        self.send_message(message["chat_id"],
                          text,
                          reply_to=message["id"],
                          parse_mode=parse_mode)

    def admin_message(self, text):
        """
        Send messages to all admins
        :param text: message text
        :type text: str or unicode
        :rtype: None
        """
        for admin_id in bot_settings.admin_ids:
            self.send_message(admin_id, text, parse_mode="html")

    def check_new_messages(self):
        """
        Checks whether new text messages present
        :return:
        :rtype: list of dict
        """
        messages = []
        for message in self.get_updates():
            if message.get('message', {}).get('text') is not None or message.get('message', {}).get('photo') is not None:
                messages.append(
                    {'id': message.get('message', {}).get('message_id'),
                     'text': message.get('message', {}).get('text'),
                     'photo': message.get('message', {}).get('photo'),
                     'from_id': message.get('message', {}).get('from', {}).get('id'),
                     'username': message.get('message', {}).get('from', {}).get('username'),
                     'chat_id': message.get('message', {}).get('chat', {}).get('id'),
                     'title': message.get('message', {}).get('chat', {}).get('title')})
        return messages

    @staticmethod
    def extract_command(message):
        """
        Return command written to bot
        :type message: dict
        :rtype: str or unicode
        """
        if message["text"].startswith('/'):
            return message["text"].split()[0].split('@')[0]
        else:
            return ''

    @staticmethod
    def extract_text(message):
        """
        Return the rest of message addressed to the bot, without command.
        :type message: dict
        :rtype: str or unicode
        """
        if TelegramDriver.extract_command(message) is not None:
            return message["text"].replace(TelegramDriver.extract_command(message), '').lstrip()
        else:
            return message["text"]

    def check_answer_from_chat_id(self, chat_id):
        """
        Return first answer to the specified chat_id or None
        :type chat_id: int
        :rtype: dict or None
        """
        for message in self.check_new_messages():
            if message["from_id"] == chat_id:
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
                time.sleep(timeouts.answer_check_interval)
                continue
            return answer

    def get_new_value(self, message, prompt_message):
        from_id = message["from_id"]
        if len(message["text"].split()) > 1:
            return message["text"].split()[1]
        else:
            if message["chat_id"] < 0:
                self.answer_message(message, SettingsMessages.GIVE_VALUE_NOW)
                return
            self.answer_message(message, prompt_message)
            return self.wait_for_answer(from_id)["text"]
