# -*- coding: utf-8 -*-
from time import sleep
from traceback import format_exc

from config.config import config
from config.timeouts import timeouts
from telegram.worker import TelegramWorker

bot = TelegramWorker()


while not bot.stopped:
    try:
        bot.process_messages()
        bot.process_game_updates()
        sleep(timeouts.process_check_interval)
    except Exception, e:
        bot.admin_message(format_exc())
        config.log_error(format_exc())
