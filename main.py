# -*- coding: utf-8 -*-
from time import sleep

from config.config import config
from telegram.worker import TelegramWorker

bot = TelegramWorker()


while not bot.stopped:
    bot.process_messages()
    bot.process_game_updates()
    sleep(config.process_check_interval)
