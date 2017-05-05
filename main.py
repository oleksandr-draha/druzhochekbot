# -*- coding: utf-8 -*-
from time import sleep
from traceback import format_exc

from config.config import config
from telegram.worker import TelegramWorker

bot = TelegramWorker()


while not bot.stopped:
    try:
        bot.process_messages()
        bot.process_game_updates()
        sleep(config.process_check_interval)
    except Exception, e:
        bot.telegram_driver.admin_message(format_exc())
