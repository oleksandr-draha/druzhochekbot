# -*- coding: utf-8 -*-
import json

import datetime

from config import config
from config.dictionary import NOT_FOR_GROUP_CHAT_MESSAGES, NO_GROUP_CHAT_MESSAGES, ACCESS_VIOLATION_MESSAGES, \
    NO_CODE_FOUND_MESSAGE, CODES_BLOCKED_MESSAGE, GAME_FINISHED_MESSAGE, BYE_MESSAGES, START_PAUSE_MESSAGES, \
    ALREADY_PAUSED_MESSAGE, END_PAUSE_MESSAGES, RESUME_MESSAGE, PAUSED_MESSAGE, LETS_GO_MESSAGES, \
    NOT_GROUP_CHAT_MESSAGES, WRONG_USER_ID_MESSAGE, DUPLICATE_USER_ID, CANNOT_DELETE_ADMIN_MESSAGE, \
    DELETE_USER_ID_MESSAGE, USER_DELETED_MESSAGE, PASS_WAS_CHANGED, DUPLICATE_PASS, ENTER_NEW_PASS, \
    DISAPPROVE_MESSAGES, STATUS_MESSAGE, PAUSED_STATUS_MESSAGES, GAME_CONNECTION_MESSAGES, \
    INFO_MESSAGE, BOT_WAS_RESET_MESSAGE, TASK_MESSAGE, NEW_HINT_MESSAGE, HINTS_APPEND, ADMIN_HELP_MESSAGE, \
    REGULAR_HELP_MESSAGE, GIVE_ME_LOGIN, GIVE_ME_PASSWORD, GIVE_ME_HOST, GIVE_ME_GAME, SETTINGS_WERE_CHANGED_MESSAGES, \
    CONNECTION_OK_MESSAGES, PLEASE_APPROVE_MESSAGES, CONNECTION_PROBLEM_MESSAGES, CHECK_SETTINGS_MESSAGES, \
    SETTINGS_WERE_SAVED_MESSAGES, SETTINGS_WERE_NOT_SAVED_MESSAGES, UNKNOWN_MESSAGES, NEW_ADMIN_WAS_ADDED, \
    NEW_FIELD_WAS_ADDED, NEW_KC_WAS_ADDED, NO_USER_ID_MESSAGE, HELLO_NEW_USER, HELLO_NEW_ADMIN, FIELD_TRIED_CODE, \
    NO_HINTS, ADMIN_CLEARED, FIELD_CLEARED, KC_CLEARED, NO_MESSAGE, WRONG_LEVEL_ID_MESSAGE, NO_TASK_ID, CONFIM_DELETEION, \
    NO_DATA_TO_DISPLAY
from game.driver import GameDriver
from game.worker import GameWorker


class TelegramProcessor:
    telegram_driver = None
    game_worker = None
    unknown_users = []

    def admin_command(self, message, do_function):
        from_id = message["from_id"]
        chat_id = message["chat_id"]
        if self.telegram_driver.is_admin(from_id):
            if chat_id < 0:
                if chat_id == self.group_chat_id:
                    self.telegram_driver.answer_message(message, NOT_FOR_GROUP_CHAT_MESSAGES)
                else:
                    self.telegram_driver.answer_message(message, NO_GROUP_CHAT_MESSAGES)
            else:
                do_function(message)
        elif config.answer_forbidden:
            self.telegram_driver.answer_message(message, ACCESS_VIOLATION_MESSAGES)

    def user_command(self, message, do_function):
        from_id = message["from_id"]
        chat_id = message["chat_id"]
        if chat_id < 0:
            if chat_id == self.group_chat_id:
                do_function(message)
            elif self.telegram_driver.is_admin(from_id):
                self.telegram_driver.answer_message(message, NO_GROUP_CHAT_MESSAGES)
            elif config.answer_forbidden:
                self.telegram_driver.answer_message(message, ACCESS_VIOLATION_MESSAGES)
        elif self.telegram_driver.is_user(from_id):
            do_function(message)
        elif config.answer_forbidden:
            self.telegram_driver.answer_message(message, ACCESS_VIOLATION_MESSAGES)

    def check_codes(self, message):
        command = self.telegram_driver.get_command(message)
        codes = message["text"].replace(command, '').rstrip().lstrip().split()
        codes = list(set(codes))
        results = ""
        if len(codes):
            results = ''
            for code in codes:
                result = self.game_worker.game_driver.try_code(code)
                if result in [CODES_BLOCKED_MESSAGE, GAME_FINISHED_MESSAGE]:
                    return result
                if result is None:
                    return
                results += result
        return results

    def check_code(self, message):
        command = self.telegram_driver.get_command(message)
        code = message["text"].replace(command, '').rstrip().lstrip()
        results = ""
        if len(code):
            results = self.game_worker.game_driver.try_code(code)
        return results

    def do_stop(self, message):
        self.telegram_driver.answer_message(message, BYE_MESSAGES)
        if self.group_chat_id is not None:
            self.telegram_driver.send_message(self.group_chat_id, BYE_MESSAGES)
        self.stopped = True

    def do_pause(self, message):
        if not self.paused:
            self.telegram_driver.answer_message(message, START_PAUSE_MESSAGES)
            self.paused = True
            config.paused = self.paused
        else:
            self.telegram_driver.answer_message(message, ALREADY_PAUSED_MESSAGE)

    def do_resume(self, message):
        if self.paused:
            self.telegram_driver.answer_message(message, END_PAUSE_MESSAGES)
            self.paused = False
            config.paused = self.paused
        else:
            self.telegram_driver.answer_message(message, RESUME_MESSAGE)

    def do_codes(self, message):
        if not self.paused:
            if len(message["text"].split()) > 1:
                result = self.check_codes(message)
                self.telegram_driver.answer_message(message, result)
                self.dublicate_code_to_group_chat(message, result)
            else:
                self.telegram_driver.answer_message(message, NO_CODE_FOUND_MESSAGE)
        else:
            self.telegram_driver.answer_message(message, PAUSED_MESSAGE)

    def do_code(self, message):
        if not self.paused:
            if len(message["text"].split()) > 1:
                result = self.check_code(message)
                self.telegram_driver.answer_message(message, result)
                self.dublicate_code_to_group_chat(message, result)
            else:
                self.telegram_driver.answer_message(message, NO_CODE_FOUND_MESSAGE)
        else:
            self.telegram_driver.answer_message(message, PAUSED_MESSAGE)

    def _do_approve(self, message):
        chat_id = message["chat_id"]
        self.telegram_driver.answer_message(message, LETS_GO_MESSAGES)
        self.group_chat_id = chat_id
        config.group_chat_id = self.group_chat_id
        self.paused = False
        config.paused = self.paused

    def approve_command(self, message):
        from_id = message["from_id"]
        chat_id = message["chat_id"]
        if self.telegram_driver.is_admin(from_id):
            if chat_id < 0:
                self._do_approve(message)
            else:
                self.telegram_driver.answer_message(message, NOT_GROUP_CHAT_MESSAGES)
        elif config.answer_forbidden:
            self.telegram_driver.answer_message(message, ACCESS_VIOLATION_MESSAGES)

    def do_add_admin(self, message):
        if len(message["text"].split()) > 1:
            admin_to_add = message["text"].split()[1]
            if not admin_to_add.isdigit():
                self.telegram_driver.answer_message(message, WRONG_USER_ID_MESSAGE)
            else:
                if self.telegram_driver.is_admin(int(admin_to_add)):
                    self.telegram_driver.answer_message(
                        message,
                        DUPLICATE_USER_ID)
                else:
                    config.add_admin_id(int(admin_to_add))
                    self.telegram_driver.admin_message(
                        NEW_ADMIN_WAS_ADDED.format(
                            user_id=admin_to_add,
                            nickname=self.telegram_driver.get_username(admin_to_add)))
                    self.telegram_driver.send_message(admin_to_add, HELLO_NEW_ADMIN)
        else:
            self.telegram_driver.answer_message(message,
                                                NO_USER_ID_MESSAGE)

    def do_add_field(self, message):
        # from_id = message["from_id"]
        if len(message["text"].split()) > 1:
            field_to_add = message["text"].split()[1]
            if not field_to_add.isdigit():
                self.telegram_driver.answer_message(message, WRONG_USER_ID_MESSAGE)
            else:
                if self.telegram_driver.is_field(int(field_to_add)):
                    self.telegram_driver.answer_message(
                        message,
                        DUPLICATE_USER_ID)
                else:
                    config.add_field_id(int(field_to_add))
                    self.telegram_driver.admin_message(
                        NEW_FIELD_WAS_ADDED.format(
                            user_id=field_to_add,
                            nickname=self.telegram_driver.get_username(field_to_add)))
                    self.telegram_driver.send_message(field_to_add, HELLO_NEW_USER)
        else:
            self.telegram_driver.answer_message(message,
                                                NO_USER_ID_MESSAGE)

    def do_add_kc(self, message):
        # from_id = message["from_id"]
        if len(message["text"].split()) > 1:
            kc_to_add = message["text"].split()[1]
            if not kc_to_add.isdigit():
                self.telegram_driver.answer_message(message, WRONG_USER_ID_MESSAGE)
            else:
                if self.telegram_driver.is_kc(int(kc_to_add)):
                    self.telegram_driver.answer_message(
                        message,
                        DUPLICATE_USER_ID)
                else:
                    config.add_kc_id(int(kc_to_add))
                    self.telegram_driver.admin_message(
                        NEW_KC_WAS_ADDED.format(
                            user_id=kc_to_add,
                            nickname=self.telegram_driver.get_username(kc_to_add)))
                    self.telegram_driver.send_message(kc_to_add, HELLO_NEW_USER)
        else:
            self.telegram_driver.answer_message(message,
                                                NO_USER_ID_MESSAGE)

    def do_delete_admin(self, message):
        from_id = message["from_id"]
        if len(config.admin_ids) == 1:
            self.telegram_driver.answer_message(message, CANNOT_DELETE_ADMIN_MESSAGE)
        else:
            if len(message["text"].split()) > 1:
                admin_to_delete = message["text"].split()[1]
            else:
                self.telegram_driver.answer_message(
                    message,
                    DELETE_USER_ID_MESSAGE.format(
                        current_ids=self.telegram_driver.get_usernames(config.admin_ids)))
                admin_to_delete = self.telegram_driver.wait_for_answer(from_id)["text"]
            if not admin_to_delete.isdigit() or int(admin_to_delete) not in config.admin_ids:
                self.telegram_driver.answer_message(message, WRONG_USER_ID_MESSAGE)
            else:
                config.delete_admin_id(int(admin_to_delete))
                self.telegram_driver.answer_message(message, USER_DELETED_MESSAGE)

    def do_delete_field(self, message):
        from_id = message["from_id"]
        if len(message["text"].split()) > 1:
            field_to_delete = message["text"].split()[1]
        else:
            self.telegram_driver.answer_message(
                message,
                DELETE_USER_ID_MESSAGE.format(
                    current_ids=self.telegram_driver.get_usernames(config.field_ids)))
            field_to_delete = self.telegram_driver.wait_for_answer(from_id)["text"]
        if not field_to_delete.isdigit() or int(field_to_delete) not in config.field_ids:
            self.telegram_driver.answer_message(message, WRONG_USER_ID_MESSAGE)
        else:
            config.delete_field_id(int(field_to_delete))
            self.telegram_driver.answer_message(message, USER_DELETED_MESSAGE)

    def do_delete_kc(self, message):
        from_id = message["from_id"]
        if len(message["text"].split()) > 1:
            kc_to_delete = message["text"].split()[1]
        else:
            self.telegram_driver.answer_message(
                message,
                DELETE_USER_ID_MESSAGE.format(
                    current_ids=self.telegram_driver.get_usernames(config.kc_ids)))
            kc_to_delete = self.telegram_driver.wait_for_answer(from_id)["text"]
        if not kc_to_delete.isdigit() or int(kc_to_delete) not in config.kc_ids:
            self.telegram_driver.answer_message(message, WRONG_USER_ID_MESSAGE)
        else:
            config.delete_kc_id(int(kc_to_delete))
            self.telegram_driver.answer_message(message, USER_DELETED_MESSAGE)

    def do_edit_admin_pass(self, message):
        from_id = message["from_id"]
        if len(message["text"].split()) > 1:
            old = config.admin_passphrase
            new = message["text"].split()[1]
            if new not in config.passphrases:
                config.admin_passphrase = message["text"].split()[1]
                self.telegram_driver.answer_message(
                    message,
                    PASS_WAS_CHANGED.format(code1=old,
                                            code2=config.admin_passphrase))
            else:
                self.telegram_driver.answer_message(
                    message,
                    DUPLICATE_PASS)
        else:
            self.telegram_driver.answer_message(
                message,
                ENTER_NEW_PASS.format(code=config.admin_passphrase))
            old = config.admin_passphrase
            new = self.telegram_driver.wait_for_answer(from_id)["text"]
            if new not in config.passphrases:
                config.admin_passphrase = new
                self.telegram_driver.answer_message(
                    message,
                    PASS_WAS_CHANGED.format(code1=old,
                                            code2=new))
            else:
                self.telegram_driver.answer_message(
                    message,
                    DUPLICATE_PASS)

    def do_edit_field_pass(self, message):
        from_id = message["from_id"]
        if len(message["text"].split()) > 1:
            old = config.field_passphrase
            new = message["text"].split()[1]
            if new not in config.passphrases:
                config.field_passphrase = message["text"].split()[1]
                self.telegram_driver.answer_message(
                    message,
                    PASS_WAS_CHANGED.format(code1=old,
                                            code2=config.field_passphrase))
            else:
                self.telegram_driver.answer_message(
                    message,
                    DUPLICATE_PASS)
        else:
            self.telegram_driver.answer_message(
                message,
                ENTER_NEW_PASS.format(code=config.field_passphrase))
            old = config.field_passphrase
            new = self.telegram_driver.wait_for_answer(from_id)["text"]
            if new not in config.passphrases:
                config.field_passphrase = new
                self.telegram_driver.answer_message(
                    message,
                    PASS_WAS_CHANGED.format(code1=old,
                                            code2=new))
            else:
                self.telegram_driver.answer_message(
                    message,
                    DUPLICATE_PASS)

    def do_edit_kc_pass(self, message):
        from_id = message["from_id"]
        if len(message["text"].split()) > 1:
            old = config.kc_passphrase
            new = message["text"].split()[1]
            if new not in config.passphrases:
                config.kc_passphrase = message["text"].split()[1]
                self.telegram_driver.answer_message(
                    message,
                    PASS_WAS_CHANGED.format(code1=old,
                                            code2=config.kc_passphrase))
            else:
                self.telegram_driver.answer_message(
                    message,
                    DUPLICATE_PASS)
        else:
            self.telegram_driver.answer_message(
                message,
                ENTER_NEW_PASS.format(code=config.kc_passphrase))
            old = config.kc_passphrase
            new = self.telegram_driver.wait_for_answer(from_id)["text"]
            if new not in config.passphrases:
                config.kc_passphrase = new
                self.telegram_driver.answer_message(
                    message,
                    PASS_WAS_CHANGED.format(code1=old,
                                            code2=new))
            else:
                self.telegram_driver.answer_message(
                    message,
                    DUPLICATE_PASS)

    def do_clearadmin(self, message):
        self.telegram_driver.answer_message(message, CONFIM_DELETEION)
        answer = self.telegram_driver.wait_for_answer(message["from_id"])
        if answer["text"] == "YES":
            config.clear_admins()
            self.telegram_driver.answer_message(message, ADMIN_CLEARED)

    def do_clearfield(self, message):
        self.telegram_driver.answer_message(message, CONFIM_DELETEION)
        answer = self.telegram_driver.wait_for_answer(message["from_id"])
        if answer["text"] == "YES":
            config.clear_fields()
            self.telegram_driver.answer_message(message, FIELD_CLEARED)

    def do_clearkc(self, message):
        self.telegram_driver.answer_message(message, CONFIM_DELETEION)
        answer = self.telegram_driver.wait_for_answer(message["from_id"])
        if answer["text"] == "YES":
            config.clear_kcs()
            self.telegram_driver.answer_message(message, KC_CLEARED)

    def do_chat_message(self, message):
        if self.group_chat_id is not None:
            message_text = self.telegram_driver.get_message_text(message)
            self.telegram_driver.send_message(
                self.group_chat_id,
                message_text)

    def do_alert(self, message):
        if self.group_chat_id is not None:
            usernames = self.telegram_driver.get_usernames(config.field_ids)
            alert_captions = ['@%s ' % username
                              for username in usernames.values()
                              if username is not None]
            alert_caption = ''.join(alert_captions) + '\r\n'
            message_text = self.telegram_driver.get_message_text(message)
            self.telegram_driver.send_message(
                self.group_chat_id,
                alert_caption + message_text)

    def do_message(self, message):
        message_text = self.telegram_driver.get_message_text(message)
        if len(message_text.split()) > 1:
            if message_text.split()[0].isdigit():
                user_id = int(message_text.split()[0])
                message_text = message_text.replace(message_text.split()[0], '').lstrip()
                self.telegram_driver.send_message(
                    user_id,
                    message_text)
            else:
                self.telegram_driver.answer_message(message,
                                                    WRONG_USER_ID_MESSAGE)
        else:
            self.telegram_driver.answer_message(message,
                                                NO_MESSAGE)

    def do_message_admin(self, message):
        message_text = self.telegram_driver.get_message_text(message)
        for admin_id in config.admin_ids:
            self.telegram_driver.send_message(admin_id,
                                              message_text)

    def do_message_field(self, message):
        message_text = self.telegram_driver.get_message_text(message)
        for field_id in config.field_ids:
            self.telegram_driver.send_message(field_id,
                                              message_text)

    def do_message_kc(self, message):
        message_text = self.telegram_driver.get_message_text(message)
        for kc_id in config.kc_ids:
            self.telegram_driver.send_message(kc_id,
                                              message_text)

    def do_send_source(self, message):
        from_id = message["from_id"]
        source = self.game_worker.game_page
        if len(source):
            self.telegram_driver.send_file(from_id,
                                           source,
                                           'source.htm')
        else:
            self.telegram_driver.answer_message(message,
                                                NO_DATA_TO_DISPLAY)

    def do_send_errors(self, message):
        from_id = message["from_id"]
        if len(config.errors):
            self.telegram_driver.send_file(from_id,
                                           str(config.repr_errors()),
                                           'errors.txt')
        else:
            self.telegram_driver.answer_message(message,
                                                NO_DATA_TO_DISPLAY)

    def do_send_unknown(self, message):
        from_id = message["from_id"]
        unknown_message = ""
        for unknown in self.unknown_users:
            unknown_message += u"{timestamp}\r\n{user_id} : {username}\r\n{message}\r\n\r\n".format(
                timestamp=unknown["timestamp"],
                user_id=unknown["user_id"],
                message=unknown["message_text"],
                username=unknown["username"])
        if len(unknown_message):
            self.telegram_driver.send_file(from_id,
                                           unknown_message,
                                           'unknown.txt')
        else:
            self.telegram_driver.answer_message(message,
                                                NO_DATA_TO_DISPLAY)

    def _do_disapprove(self, message):
        self.group_chat_id = None
        config.group_chat_id = self.group_chat_id
        self.paused = False
        config.paused = self.paused
        self.telegram_driver.answer_message(message, DISAPPROVE_MESSAGES)

    def disapprove_command(self, message):
        from_id = message["from_id"]
        chat_id = message["chat_id"]
        if self.telegram_driver.is_admin(from_id):
            if chat_id < 0:
                if chat_id == self.group_chat_id:
                    self._do_disapprove(message)
                else:
                    self.telegram_driver.answer_message(message, NO_GROUP_CHAT_MESSAGES)
            else:
                self.telegram_driver.answer_message(message, NOT_GROUP_CHAT_MESSAGES)
        elif config.answer_forbidden:
            self.telegram_driver.answer_message(message, ACCESS_VIOLATION_MESSAGES)

    def do_status(self, message):
        hints_shown = ''
        for i in self.game_worker.hints_shown:
            hints_shown += str(i) + ' '
        status_message = STATUS_MESSAGE.format(
            paused=PAUSED_STATUS_MESSAGES[self.paused],
            chat_id=self.group_chat_id,
            game_connection=GAME_CONNECTION_MESSAGES[self.game_worker.game_driver.is_logged()],
            game_level_id=self.game_worker.last_level_shown,
            game_hint_id=hints_shown
        )
        self.telegram_driver.answer_message(message, status_message)

    def do_info(self, message):
        info_message = INFO_MESSAGE.format(
            chat_id=self.group_chat_id,
            login=self.game_worker.game_driver.login,
            password=self.game_worker.game_driver.password,
            host=self.game_worker.game_driver.host,
            game_id=self.game_worker.game_driver.game_id,
            admins=json.dumps(self.telegram_driver.get_usernames(config.admin_ids)),
            fields=json.dumps(self.telegram_driver.get_usernames(config.field_ids)),
            kcs=json.dumps(self.telegram_driver.get_usernames(config.kc_ids)),
            admin_passphrase=config.admin_passphrase,
            field_passphrase=config.field_passphrase,
            kc_passphrase=config.kc_passphrase,
            time_start=config.start_time,
            bot_errors=len(config.errors),
            unknown_users=len(self.unknown_users))
        self.telegram_driver.answer_message(message, info_message)

    def do_reset(self, message):
        self.game_worker.reset_level()
        self.telegram_driver.answer_message(message, BOT_WAS_RESET_MESSAGE)

    def do_task(self, message):
        if len(message["text"].split()) > 1:
            level_to_show = int(message["text"].split()[1])
            task_text = self.game_worker.tasks_received.get(level_to_show,
                                                            WRONG_LEVEL_ID_MESSAGE)
        else:
            task_text = TASK_MESSAGE.format(
                level_number=self.game_worker.last_level_shown,
                task=self.game_worker.last_task_text)
        self.telegram_driver.answer_message(message, task_text, parse_mode="HTML")

    def do_codes_history(self, message):
        if len(message["text"].split()) > 1:
            level_to_show = int(message["text"].split()[1])
            task_text = self.game_worker.game_driver.codes_entered.get(level_to_show)
            if task_text is not None:
                codes = '\r\n'.join(task_text)
            else:
                codes = WRONG_LEVEL_ID_MESSAGE
            self.telegram_driver.answer_message(message, codes)
        else:
            self.telegram_driver.answer_message(message, NO_TASK_ID)

    def do_hints(self, message):
        hints = []
        for hint_id in sorted(self.game_worker.all_hints.keys()):
            hints.append(NEW_HINT_MESSAGE.format(
                smile=HINTS_APPEND,
                hint_number=hint_id,
                hint=self.game_worker.all_hints[hint_id]))
        for hint in hints:
            self.telegram_driver.answer_message(message, hint, parse_mode="HTML")
        else:
            self.telegram_driver.answer_message(message, NO_HINTS, parse_mode="HTML")

    def do_help(self, message):
        from_id = message["from_id"]
        if self.telegram_driver.is_admin(from_id):
            self.telegram_driver.answer_message(message, ADMIN_HELP_MESSAGE)
        else:
            self.telegram_driver.answer_message(message, REGULAR_HELP_MESSAGE)

    def do_gap(self, message):
        codes_gap = self.game_worker.game_driver.get_codes_gap()
        self.telegram_driver.answer_message(message,
                                            codes_gap)

    def do_edit_settings(self, message):
        from_id = message["from_id"]

        self.telegram_driver.send_message(
            from_id,
            GIVE_ME_LOGIN)
        GameDriver.login = self.telegram_driver.wait_for_answer(from_id)["text"]
        config.game_login = GameDriver.login
        self.telegram_driver.send_message(
            from_id,
            GIVE_ME_PASSWORD)
        GameDriver.password = self.telegram_driver.wait_for_answer(from_id)["text"]
        config.game_password = GameDriver.password
        self.telegram_driver.send_message(
            from_id,
            GIVE_ME_HOST)
        GameDriver.host = self.telegram_driver.wait_for_answer(from_id)["text"]
        config.game_host = GameDriver.host
        self.telegram_driver.send_message(
            from_id,
            GIVE_ME_GAME)
        GameDriver.game_id = self.telegram_driver.wait_for_answer(from_id)["text"]
        config.game_id = GameDriver.game_id

        self.game_worker = GameWorker()
        self.paused = True
        config.paused = self.paused
        self.telegram_driver.admin_message(SETTINGS_WERE_CHANGED_MESSAGES)
        if self.game_worker.connected:
            self.telegram_driver.admin_message(CONNECTION_OK_MESSAGES)
            self.telegram_driver.admin_message(PLEASE_APPROVE_MESSAGES)
            self.do_reset(message)
            self.paused = False
            config.paused = self.paused
            return True
        else:
            self.telegram_driver.admin_message(CONNECTION_PROBLEM_MESSAGES)
            self.telegram_driver.admin_message(CHECK_SETTINGS_MESSAGES)
            return False

    def do_save_settings(self, message):
        result = config.save_config()
        if result:
            self.telegram_driver.answer_message(message, SETTINGS_WERE_SAVED_MESSAGES)
        else:
            self.telegram_driver.answer_message(message, SETTINGS_WERE_NOT_SAVED_MESSAGES)

    def unknown_command(self, message):
        if config.answer_unknown:
            self.telegram_driver.answer_message(message, UNKNOWN_MESSAGES)

    def process_unknown_user(self, message):
        from_id = message["from_id"]
        if from_id not in config.admin_ids + config.field_ids + config.kc_ids:
            self.unknown_users.append({"timestamp": datetime.datetime.now(),
                                       "user_id": from_id,
                                       "username": message["username"],
                                       "message_text": message["text"]})
            if len(self.unknown_users) > 100:
                self.unknown_users[from_id].pop(0)
            return True
        else:
            return False

    def process_new_user(self, message):
        passphrase = message["text"]
        from_id = message["from_id"]
        if passphrase == config.admin_passphrase:
            if from_id in config.admin_ids:
                self.telegram_driver.answer_message(message, DUPLICATE_USER_ID)
            else:
                config.add_admin_id(int(from_id))
                self.telegram_driver.answer_message(message, HELLO_NEW_ADMIN)
                self.telegram_driver.admin_message(
                    NEW_ADMIN_WAS_ADDED.format(user_id=from_id,
                                               nickname=self.telegram_driver.get_username(from_id)))
                return True
        elif passphrase == config.field_passphrase:
            if from_id in config.field_ids:
                self.telegram_driver.answer_message(message, DUPLICATE_USER_ID)
            else:
                config.add_field_id(int(from_id))
                self.telegram_driver.answer_message(message, HELLO_NEW_USER)
                self.telegram_driver.admin_message(
                    NEW_FIELD_WAS_ADDED.format(user_id=from_id,
                                               nickname=self.telegram_driver.get_username(from_id)))
                return True
        elif passphrase == config.kc_passphrase:
            if from_id in config.kc_ids:
                self.telegram_driver.answer_message(message, DUPLICATE_USER_ID)
            else:
                config.add_kc_id(int(from_id))
                self.telegram_driver.answer_message(message, HELLO_NEW_USER)
                self.telegram_driver.admin_message(
                    NEW_KC_WAS_ADDED.format(user_id=from_id,
                                            nickname=self.telegram_driver.get_username(from_id)))
                return True
        else:
            return False

    def dublicate_code_to_group_chat(self, message, result):
        from_id = message["from_id"]
        if self.telegram_driver.is_field(from_id) \
                and self.group_chat_id is not None \
                and message["chat_id"] != self.group_chat_id \
                and result is not None:
            self.telegram_driver.send_message(
                self.group_chat_id,
                FIELD_TRIED_CODE.format(
                    nickname=self.telegram_driver.get_username(from_id),
                    codes=result))

    def process_code_simple_message(self, message):
        from_id = message["from_id"]
        if from_id in config.field_ids:
            if not message['text'].startswith('/'):
                result = self.check_code(message)
                self.telegram_driver.answer_message(message, result)
                self.dublicate_code_to_group_chat(message, result)
        elif from_id in config.kc_ids:
            if not message['text'].startswith('/'):
                result = self.check_code(message)
                self.telegram_driver.answer_message(message, result)
