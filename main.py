# -*- coding: utf-8 -*-
from traceback import format_exc

from datetime import timedelta, datetime

from config import errors_log, timeouts, activity_log, bot_settings
from telegram.worker import TelegramWorker

bot = TelegramWorker()

current_time = datetime.now()
next_run = current_time


while not bot.stopped:
    if bot_settings.log_activity:
        activity_log.log_activity()
    try:
        bot.process_messages()
        if next_run < datetime.now():
            bot.process_game_updates()
            bot.process_codes_queue()
            next_run = datetime.now() + timedelta(seconds=timeouts.process_check_interval)
    except Exception, e:
        bot.admin_message(format_exc())
        errors_log.log_error(format_exc())
