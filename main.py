# -*- coding: utf-8 -*-
from traceback import format_exc

from datetime import timedelta, datetime

from config import errors_log, timeouts, activity_log, bot_settings
from telegram.worker import TelegramWorker

bot = TelegramWorker()

current_time = datetime.now()
game_update_next_run = current_time
code_enter_next_run = current_time


while not bot.stopped:
    if bot_settings.log_activity:
        activity_log.log_activity()
    try:
        bot.process_messages()
        game_page = None
        if code_enter_next_run < datetime.now():
            game_page = bot.process_codes_queue()
            game_page = bot.process_codes_queue()
            game_page = bot.process_codes_queue()
            code_enter_next_run = datetime.now() + timedelta(seconds=timeouts.codes_interval)
        if game_update_next_run < datetime.now():
            bot.process_game_updates(game_page=game_page)
            game_update_next_run = datetime.now() + timedelta(seconds=timeouts.game_update_check_interval)
    except Exception, e:
        bot.admin_message(format_exc())
        errors_log.log_error(format_exc())
