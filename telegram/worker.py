# -*- coding: utf-8 -*-
from config.config import config
from config.dictionary import SettingsMessages
from telegram.processors import TelegramProcessor


class TelegramWorker(TelegramProcessor):
    def process_messages(self):
        for message in self.check_new_messages():
            # Process high-level events:
            # 1. Adding new user by invite code
            # 2. Ignore message if it was received from non-authorized iser
            # 3. Try to enter code from field user
            if self.process_new_user(message):
                continue
            if self.process_unknown_user(message):
                continue
            self.process_code_simple_message(message)

            command = self.extract_command(message).lower()
            # region User commands:
            if command in config.code_command:
                self._user_command(message, self.do_code)
            elif command in config.codes_command:
                self._user_command(message, self.do_codes)
            elif command == config.status_command:
                self._user_command(message, self.do_status)
            elif command == config.task_command:
                self._user_command(message, self.do_task)
            elif command == config.codes_history_command:
                self._user_command(message, self.do_codes_history)
            elif command == config.hints_command:
                self._user_command(message, self.do_hints)
            elif command == config.help_command:
                self._user_command(message, self.do_help)
            elif command == config.gap_command:
                self._user_command(message, self.do_gap)
            # endregion

            # region Admin in chat commands:
            elif command == config.stop_command:
                self._admin_in_group_chat_command(message, self.do_stop)
            elif command == config.resume_command:
                self._admin_in_group_chat_command(message, self.do_resume)
            elif command == config.pause_command:
                self._admin_in_group_chat_command(message, self.do_pause)
            elif command == config.reset_command:
                self._admin_in_group_chat_command(message, self.do_reset)
            elif command == config.chat_message_command:
                self._admin_in_group_chat_command(message, self.do_chat_message)
            elif command == config.alert_command:
                self._admin_in_group_chat_command(message, self.do_alert)
            elif command == config.message_admin_command:
                self._admin_in_group_chat_command(message, self.do_message_admin)
            elif command == config.message_field_command:
                self._admin_in_group_chat_command(message, self.do_message_field)
            elif command == config.message_kc_command:
                self._admin_in_group_chat_command(message, self.do_message_kc)
            # endregion

            # region Admin commands:
            elif command == config.approve_command:
                self.approve_command(message)
            elif command == config.disapprove_command:
                self.disapprove_command(message)
            elif command == config.info_command:
                self._admin_command(message, self.do_info)
            elif command == config.edit_command:
                self._admin_command(message, self.do_edit_settings)
            elif command == config.save_command:
                self._admin_command(message, self.do_save_settings)
            elif command == config.add_admin_command:
                self._admin_command(message, self.do_add_admin)
            elif command == config.delete_admin_command:
                self._admin_command(message, self.do_delete_admin)
            elif command == config.add_field_command:
                self._admin_command(message, self.do_add_field)
            elif command == config.delete_field_command:
                self._admin_command(message, self.do_delete_field)
            elif command == config.add_kc_command:
                self._admin_command(message, self.do_add_kc)
            elif command == config.delete_kc_command:
                self._admin_command(message, self.do_delete_kc)
            elif command == config.edit_admin_pass:
                self._admin_command(message, self.do_edit_admin_pass)
            elif command == config.edit_field_pass:
                self._admin_command(message, self.do_edit_field_pass)
            elif command == config.edit_kc_pass:
                self._admin_command(message, self.do_edit_kc_pass)
            elif command == config.clearadmin_command:
                self._admin_command(message, self.do_clearadmin)
            elif command == config.clearfield_command:
                self._admin_command(message, self.do_clearfield)
            elif command == config.clearkc_command:
                self._admin_command(message, self.do_clearkc)
            elif command == config.message_command:
                self._admin_command(message, self.do_message)
            elif command == config.token_command:
                self._admin_command(message, self.do_token)
            elif command == config.codes_limit_command:
                self._admin_command(message, self.do_codes_limit)
            elif command == config.login_command:
                self._admin_command(message, self.do_change_login)
            elif command == config.pass_command:
                self._admin_command(message, self.do_change_pass)
            elif command == config.host_command:
                self._admin_command(message, self.do_change_host)
            elif command == config.game_command:
                self._admin_command(message, self.do_change_game)
            elif command == config.send_source_command:
                self._admin_command(message, self.do_send_source)
            elif command == config.send_errors_command:
                self._admin_command(message, self.do_send_errors)
            elif command == config.send_unknown_command:
                self._admin_command(message, self.do_send_unknown)
            else:
                self.unknown_command(message)
            # endregion

    def process_game_updates(self):
        if not self.paused and self.group_chat_id is not None:
            updates = self.game_worker.check_updates()
            if updates is None:
                self.admin_message(SettingsMessages.CONNECTION_PROBLEM)
            else:
                for update in updates:
                    self.send_message(self.group_chat_id,
                                      update,
                                      parse_mode="HTML")
