# -*- coding: utf-8 -*-
from time import sleep

from telegram.worker import TelegramWorker

bot = TelegramWorker()

initialized = bot.setup_bot()
while not initialized:
    initialized = bot.setup_bot()

while not bot.stopped and initialized is not None:
    bot.process_messages()
    bot.process_game_tasks()
    sleep(1)
