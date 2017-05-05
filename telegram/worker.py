# -*- coding: utf-8 -*-
from config.config import config
from config.dictionary import CONNECTION_PROBLEM_MESSAGES, \
    CONNECTION_OK_MESSAGES, PLEASE_APPROVE_MESSAGES, CHECK_SETTINGS_MESSAGES
from game.driver import GameDriver
from game.worker import GameWorker
from telegram.driver import TelegramDriver
from telegram.processors import TelegramProcessor


class TelegramWorker(TelegramProcessor):
    def __init__(self):
        self.telegram_driver = TelegramDriver()
        self.telegram_driver.get_updates()
        self.initial_message = None
        self.initialize_attempts = 0
        self.paused = False
        self.stopped = False
        self.game_worker = None
        self.group_chat_id = None
        self.add_admin_passphrase = None
        self.add_field_passphrase = None
        self.add_kc_passphrase = None

        # Messages dictionary

        self.load_settings()

    def load_settings(self):
        GameDriver.login = config.game_login
        GameDriver.password = config.game_password
        GameDriver.game_id = config.game_id
        GameDriver.host = config.game_host
        self.game_worker = GameWorker()
        if self.game_worker.connected:
            self.telegram_driver.admin_message(CONNECTION_OK_MESSAGES)
            self.telegram_driver.admin_message(PLEASE_APPROVE_MESSAGES)
            return True
        else:
            self.telegram_driver.admin_message(CONNECTION_PROBLEM_MESSAGES)
            self.telegram_driver.admin_message(CHECK_SETTINGS_MESSAGES)
            return False

    def process_messages(self):
        for message in self.telegram_driver.check_new_messages():
            if self.initial_message is None:
                self.initial_message = message
            command = self.telegram_driver.get_command(message)
            if self.process_new_user(message) is None:
                continue
            self.process_code_simple_message(message)
            # User commands:
            if command in config.code_command:
                self.user_command(message, self.do_code)
            elif command in config.codes_command:
                self.user_command(message, self.do_codes)
            elif command == config.status_command:
                self.user_command(message, self.do_status)
            elif command == config.task_command:
                self.user_command(message, self.do_task)
            elif command == config.hints_command:
                self.user_command(message, self.do_hints)
            elif command == config.help_command:
                self.user_command(message, self.do_help)
            elif command == config.gap_command:
                self.user_command(message, self.do_gap)

            # Admin commands:
            elif command == config.approve_command:
                self.approve_command(message)
            elif command == config.disapprove_command:
                self.disapprove_command(message)
            elif command == config.stop_command:
                self.admin_command(message, self.do_stop)
            elif command == config.resume_command:
                self.admin_command(message, self.do_resume)
            elif command == config.pause_command:
                self.admin_command(message, self.do_pause)
            elif command == config.info_command:
                self.admin_command(message, self.do_info)
            elif command == config.reset_command:
                self.admin_command(message, self.do_reset)
            elif command == config.edit_command:
                self.admin_command(message, self.do_edit_settings)
            elif command == config.save_command:
                self.admin_command(message, self.do_save_settings)
            elif command == config.add_admin_command:
                self.admin_command(message, self.do_add_admin)
            elif command == config.delete_admin_command:
                self.admin_command(message, self.do_delete_admin)
            elif command == config.add_field_command:
                self.admin_command(message, self.do_add_field)
            elif command == config.delete_field_command:
                self.admin_command(message, self.do_delete_field)
            elif command == config.add_kc_command:
                self.admin_command(message, self.do_add_kc)
            elif command == config.delete_kc_command:
                self.admin_command(message, self.do_delete_kc)
            elif command == config.edit_admin_pass:
                self.admin_command(message, self.do_edit_admin_pass)
            elif command == config.edit_field_pass:
                self.admin_command(message, self.do_edit_field_pass)
            elif command == config.edit_kc_pass:
                self.admin_command(message, self.do_edit_kc_pass)
            elif command == config.clearadmin_command:
                self.admin_command(message, self.do_clearadmin)
            elif command == config.clearfield_command:
                self.admin_command(message, self.do_clearfield)
            elif command == config.clearkc_command:
                self.admin_command(message, self.do_clearkc)
            else:
                self.unknown_command(message)

    def process_game_updates(self):
        if not self.paused and self.group_chat_id is not None:
            updates = self.game_worker.check_updates()
            if updates is None:
                self.telegram_driver.admin_message(CONNECTION_PROBLEM_MESSAGES)
            else:
                for update in updates:
                    self.telegram_driver.send_message(self.group_chat_id,
                                                      update,
                                                      parse_mode="HTML")
