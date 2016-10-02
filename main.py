# -*- coding: utf-8 -*-
from telegram_worker import TelegramWorker



bot = TelegramWorker()

while True:
    bot.process_messages()