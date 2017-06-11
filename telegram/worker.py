# -*- coding: utf-8 -*-
from config import bot_settings, commands
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
            if command in commands.code:
                self._user_command(message, self.do_code)
            elif command in commands.codes_:
                self._user_command(message, self.do_codes)
            elif command == commands.status:
                self._user_command(message, self.do_status)
            elif command == commands.task:
                self._user_command(message, self.do_task)
            elif command == commands.tasks_all:
                self._user_command(message, self.do_tasks_all)
            elif command == commands.task_html:
                self._user_command(message, self.do_task_html)
            elif command == commands.codes_history:
                self._user_command(message, self.do_codes_history)
            elif command == commands.codes_all:
                self._user_command(message, self.do_codes_all)
            elif command == commands.hints:
                self._user_command(message, self.do_hints)
            elif command == commands.help:
                self._user_command(message, self.do_help)
            elif command == commands.gap:
                self._user_command(message, self.do_gap)
            elif command == commands.codes_statistic:
                self._user_command(message, self.do_codes_statistic)
            # endregion

            # region Admin in chat commands:
            elif command == commands.approve:
                self.approve_command(message)
            elif command == commands.disapprove:
                self.disapprove_command(message)
            elif command == commands.stop:
                self._admin_in_group_chat_command(message, self.do_stop)
            elif command == commands.resume:
                self._admin_in_group_chat_command(message, self.do_resume)
            elif command == commands.pause:
                self._admin_in_group_chat_command(message, self.do_pause)
            elif command == commands.reset:
                self._admin_in_group_chat_command(message, self.do_reset)
            elif command == commands.chat_message:
                self._admin_in_group_chat_command(message, self.do_chat_message)
            elif command == commands.alert:
                self._admin_in_group_chat_command(message, self.do_alert)
            elif command == commands.message_admin:
                self._admin_in_group_chat_command(message, self.do_message_admin)
            elif command == commands.message_field:
                self._admin_in_group_chat_command(message, self.do_message_field)
            elif command == commands.message_kc:
                self._admin_in_group_chat_command(message, self.do_message_kc)
            elif command == commands.autohandbrake_:
                self._admin_in_group_chat_command(message, self.do_set_autohandbrake)
            elif command == commands.handbrake_set:
                self._admin_in_group_chat_command(message, self.do_set_handbrake)
            elif command == commands.codes:
                self._admin_in_group_chat_command(message, self.do_codes_limit)
            # endregion

            # region Admin commands:
            elif command == commands.set_group_chat:
                self._admin_command(message, self.do_set_group_chat)
            elif command == commands.info:
                self._admin_command(message, self.do_info)
            elif command == commands.edit:
                self._admin_command(message, self.do_edit_settings)
            elif command == commands.add_admin:
                self._admin_command(message, self.do_add_admin)
            elif command == commands.delete_admin:
                self._admin_command(message, self.do_delete_admin)
            elif command == commands.add_field:
                self._admin_command(message, self.do_add_field)
            elif command == commands.delete_field:
                self._admin_command(message, self.do_delete_field)
            elif command == commands.add_kc:
                self._admin_command(message, self.do_add_kc)
            elif command == commands.delete_kc:
                self._admin_command(message, self.do_delete_kc)
            elif command == commands.edit_admin_pass:
                self._admin_command(message, self.do_edit_admin_pass)
            elif command == commands.edit_field_pass:
                self._admin_command(message, self.do_edit_field_pass)
            elif command == commands.edit_kc_pass:
                self._admin_command(message, self.do_edit_kc_pass)
            elif command == commands.clean_admin:
                self._admin_command(message, self.do_cleanadmin)
            elif command == commands.clean_field:
                self._admin_command(message, self.do_cleanfield)
            elif command == commands.clean_kc:
                self._admin_command(message, self.do_cleankc)
            elif command == commands.message:
                self._admin_command(message, self.do_message)
            elif command == commands.token:
                self._admin_command(message, self.do_token)
            elif command == commands.login:
                self._admin_command(message, self.do_change_login)
            elif command == commands.passwords:
                self._admin_command(message, self.do_change_pass)
            elif command == commands.host:
                self._admin_command(message, self.do_change_host)
            elif command == commands.game:
                self._admin_command(message, self.do_change_game)
            elif command == commands.send_source:
                self._admin_command(message, self.do_send_source)
            elif command == commands.send_errors:
                self._admin_command(message, self.do_send_errors)
            elif command == commands.clean_errors_:
                self._admin_command(message, self.do_clean_errors)
            elif command == commands.send_unknown:
                self._admin_command(message, self.do_send_unknown)
            elif command == commands.clean_unknown:
                self._admin_command(message, self.do_clean_unknown)
            elif command == commands.clean_memory:
                self._admin_command(message, self.do_clean_memory)
            elif command == commands.tag_field_:
                self._admin_command(message, self.do_set_tag_field)
            elif command == commands.log_activity:
                self._admin_command(message, self.do_set_log_activity)
            else:
                self.unknown_command(message)
            # endregion

    def process_game_updates(self):
        if not bot_settings.paused and bot_settings.group_chat_id is not None:
            last_level_shown = self.game_worker.last_level_shown
            updates = self.game_worker.check_updates()
            current_level = self.game_worker.last_level_shown
            if updates is None:
                self.admin_message(SettingsMessages.CONNECTION_PROBLEM)
            else:
                game_updates = ""
                for update in updates:
                    game_updates += update
                if last_level_shown != current_level:
                    if bot_settings.tag_field:
                        game_updates += self.get_alert_captions()
                self.send_message(bot_settings.group_chat_id,
                                  game_updates,
                                  parse_mode="HTML")
