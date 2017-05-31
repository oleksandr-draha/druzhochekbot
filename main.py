# -*- coding: utf-8 -*-
from traceback import format_exc

from datetime import timedelta, datetime

from config import errors_log, timeouts
from telegram.worker import TelegramWorker

bot = TelegramWorker()

current_time = datetime.now()
next_run = current_time


while not bot.stopped:
    try:
        bot.process_messages()
        if next_run < datetime.now():
            bot.process_game_updates()
            next_run = datetime.now() + timedelta(seconds=timeouts.process_check_interval)
    except Exception, e:
        bot.admin_message(format_exc())
        errors_log.log_error(format_exc())
