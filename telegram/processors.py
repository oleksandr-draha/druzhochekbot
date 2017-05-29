# -*- coding: utf-8 -*-
import json

import datetime

from config import config
from config.dictionary import Smiles, CommonMessages, BotSystemMessages, CommandMessages, SettingsMessages, \
    UserMessages, GameMessages, FileMessages, HelpMessages
from game.driver import GameDriver
from game.worker import GameWorker
from telegram.abstract_processors import AbstractProcessors


class TelegramProcessor(AbstractProcessors):
    def check_codes(self, message):
        command = self.extract_command(message)
        username = message["username"]
        codes = message["text"].replace(command, '').rstrip().lstrip().split()
        codes = [code.lower() for code in codes]
        codes = list(set(codes))
        results = ""
        if len(codes):
            results = ''
            for code in codes:
                result = self.game_worker.game_driver.try_code(code, username)
                if result in [GameMessages.CODES_BLOCKED,
                              GameMessages.GAME_FINISHED,
                              GameMessages.GAME_NOT_PAYED,
                              GameMessages.GAME_NOT_STARTED,
                              GameMessages.HANDBRAKE]:
                    return result
                if result is None:
                    return
                results += result
        return results

    def check_code(self, message):
        command = self.extract_command(message)
        username = message["username"]
        code = message["text"].replace(command, '').rstrip().lstrip().lower()
        results = ""
        if len(code):
            results = self.game_worker.game_driver.try_code(code, username)
        return results

    def do_stop(self, message):
        self.answer_message(message, CommonMessages.BYE)
        self.stopped = True

    def do_pause(self, message):
        if not self.paused:
            self.answer_message(message, CommonMessages.DO_PAUSE)
            self.paused = True
            config.paused = self.paused
        else:
            self.answer_message(message, CommonMessages.ALREADY_PAUSED)

    def do_resume(self, message):
        if self.paused:
            self.answer_message(message, CommonMessages.DO_RESUME)
            self.paused = False
            config.paused = self.paused
        else:
            self.answer_message(message, CommonMessages.ALREADY_WORKING)

    def do_codes(self, message):
        if not self.paused:
            if len(message["text"].split()) > 1:
                if len(message["text"].split()) <= config.code_limit + 1:
                    result = self.check_codes(message)
                    self.answer_message(message, result)
                    self.dublicate_code_to_group_chat(message, result)
                else:
                    self.answer_message(
                        message,
                        CommandMessages.CODE_LIMIT.format(codelimit=config.code_limit))
            else:
                self.answer_message(message, CommandMessages.NO_CODE_FOUND)
        else:
            self.answer_message(message, CommonMessages.PAUSED)

    def do_code(self, message):
        if not self.paused:
            if len(message["text"].split()) > 1:
                result = self.check_code(message)
                self.answer_message(message, result)
                self.dublicate_code_to_group_chat(message, result)
            else:
                self.answer_message(message, CommandMessages.NO_CODE_FOUND)
        else:
            self.answer_message(message, CommonMessages.PAUSED)

    def _do_approve(self, message):
        chat_id = message["chat_id"]
        self.answer_message(message, CommonMessages.LETS_GO)
        self.group_chat_id = chat_id
        config.group_chat_id = self.group_chat_id
        self.paused = False
        config.paused = self.paused

    def approve_command(self, message):
        from_id = message["from_id"]
        chat_id = message["chat_id"]
        if config.is_admin(from_id):
            if chat_id < 0:
                self._do_approve(message)
            else:
                self.answer_message(message, CommonMessages.NOT_GROUP_CHAT)
        elif config.answer_forbidden:
            self.answer_message(message, CommonMessages.ACCESS_VIOLATION_MESSAGES)

    def do_add_admin(self, message):
        if len(message["text"].split()) > 1:
            admin_to_add = message["text"].split()[1]
            if not admin_to_add.isdigit():
                self.answer_message(message, UserMessages.WRONG_USER_ID)
            else:
                if config.is_admin(int(admin_to_add)):
                    self.answer_message(
                        message,
                        UserMessages.DUPLICATE_USER_ID)
                else:
                    config.add_admin_id(int(admin_to_add))
                    self.admin_message(
                        UserMessages.NEW_ADMIN_WAS_ADDED.format(
                            user_id=admin_to_add,
                            nickname=self.get_username(admin_to_add)))
                    self.send_message(admin_to_add, UserMessages.HELLO_NEW_ADMIN)
        else:
            self.answer_message(message,
                                CommandMessages.NO_USER_ID)

    def do_set_group_chat(self, message):
        if len(message["text"].split()) > 1:
            group_chat_id = message["text"].split()[1]
            if group_chat_id.startswith("-") and group_chat_id[1:].isdigit():
                self.group_chat_id = int(group_chat_id)
                config.group_chat_id = self.group_chat_id
            else:
                self.answer_message(message, UserMessages.WRONG_USER_ID)
        else:
            self.answer_message(message,
                                CommandMessages.NO_USER_ID)

    def do_add_field(self, message):
        if len(message["text"].split()) > 1:
            field_to_add = message["text"].split()[1]
            if not field_to_add.isdigit():
                self.answer_message(message, UserMessages.WRONG_USER_ID)
            else:
                if config.is_field(int(field_to_add)):
                    self.answer_message(
                        message,
                        UserMessages.DUPLICATE_USER_ID)
                else:
                    config.add_field_id(int(field_to_add))
                    self.admin_message(
                        UserMessages.NEW_FIELD_WAS_ADDED.format(
                            user_id=field_to_add,
                            nickname=self.get_username(field_to_add)))
                    self.send_message(field_to_add, UserMessages.HELLO_NEW_USER)
        else:
            self.answer_message(message,
                                CommandMessages.NO_USER_ID)

    def do_add_kc(self, message):
        if len(message["text"].split()) > 1:
            kc_to_add = message["text"].split()[1]
            if not kc_to_add.isdigit():
                self.answer_message(message, UserMessages.WRONG_USER_ID)
            else:
                if config.is_kc(int(kc_to_add)):
                    self.answer_message(
                        message,
                        UserMessages.DUPLICATE_USER_ID)
                else:
                    config.add_kc_id(int(kc_to_add))
                    self.admin_message(
                        UserMessages.NEW_KC_WAS_ADDED.format(
                            user_id=kc_to_add,
                            nickname=self.get_username(kc_to_add)))
                    self.send_message(kc_to_add, UserMessages.HELLO_NEW_USER)
        else:
            self.answer_message(message,
                                CommandMessages.NO_USER_ID)

    def do_delete_admin(self, message):
        if len(config.admin_ids) == 1:
            self.answer_message(message, UserMessages.CANNOT_DELETE_ADMIN)
        else:
            admin_to_delete = self.get_new_value(
                message,
                UserMessages.DELETE_USER_ID.format(
                    current_ids=self.get_usernames(config.admin_ids)))
            if not admin_to_delete.isdigit() or int(admin_to_delete) not in config.admin_ids:
                self.answer_message(message, UserMessages.WRONG_USER_ID)
            else:
                config.delete_admin_id(int(admin_to_delete))
                self.answer_message(message, UserMessages.USER_DELETED)

    def do_delete_field(self, message):
        field_to_delete = self.get_new_value(
            message,
            UserMessages.DELETE_USER_ID.format(
                current_ids=self.get_usernames(config.field_ids)))
        if not field_to_delete.isdigit() or int(field_to_delete) not in config.field_ids:
            self.answer_message(message, UserMessages.WRONG_USER_ID)
        else:
            config.delete_field_id(int(field_to_delete))
            self.answer_message(message, UserMessages.USER_DELETED)

    def do_delete_kc(self, message):
        kc_to_delete = self.get_new_value(
            message,
            UserMessages.DELETE_USER_ID.format(
                current_ids=self.get_usernames(config.kc_ids)))
        if not kc_to_delete.isdigit() or int(kc_to_delete) not in config.kc_ids:
            self.answer_message(message, UserMessages.WRONG_USER_ID)
        else:
            config.delete_kc_id(int(kc_to_delete))
            self.answer_message(message, UserMessages.USER_DELETED)

    def do_edit_admin_pass(self, message):
        new = self.get_new_value(
            message,
            SettingsMessages.ENTER_NEW_PASS.format(code=config.admin_passphrase))
        old = config.admin_passphrase
        if new not in config.passphrases:
            config.admin_passphrase = new
            self.answer_message(
                message,
                SettingsMessages.PASS_WAS_CHANGED.format(code1=old,
                                                         code2=new))
        else:
            self.answer_message(
                message,
                SettingsMessages.DUPLICATE_PASS)

    def do_edit_field_pass(self, message):
        new = self.get_new_value(
            message,
            SettingsMessages.ENTER_NEW_PASS.format(code=config.field_passphrase))
        old = config.field_passphrase
        if new not in config.passphrases:
            config.field_passphrase = new
            self.answer_message(
                message,
                SettingsMessages.PASS_WAS_CHANGED.format(code1=old,
                                                         code2=new))
        else:
            self.answer_message(
                message,
                SettingsMessages.DUPLICATE_PASS)

    def do_edit_kc_pass(self, message):
        new = self.get_new_value(
            message,
            SettingsMessages.ENTER_NEW_PASS.format(code=config.kc_passphrase))
        old = config.kc_passphrase
        if new not in config.passphrases:
            config.kc_passphrase = new
            self.answer_message(
                message,
                SettingsMessages.PASS_WAS_CHANGED.format(code1=old,
                                                         code2=new))
        else:
            self.answer_message(
                message,
                SettingsMessages.DUPLICATE_PASS)

    def do_cleanadmin(self, message):
        self.answer_message(message, BotSystemMessages.CONFIRM_DELETEION)
        answer = self.wait_for_answer(message["from_id"])
        if answer["text"] == "YES":
            config.clean_admins()
            self.answer_message(message, BotSystemMessages.ADMIN_CLEARED)
        else:
            self.answer_message(message, BotSystemMessages.OPERATION_CANCELLED)

    def do_cleanfield(self, message):
        self.answer_message(message, BotSystemMessages.CONFIRM_DELETEION)
        answer = self.wait_for_answer(message["from_id"])
        if answer["text"] == "YES":
            config.clean_fields()
            self.answer_message(message, BotSystemMessages.FIELD_CLEARED)
        else:
            self.answer_message(message, BotSystemMessages.OPERATION_CANCELLED)

    def do_cleankc(self, message):
        self.answer_message(message, BotSystemMessages.CONFIRM_DELETEION)
        answer = self.wait_for_answer(message["from_id"])
        if answer["text"] == "YES":
            config.clean_kcs()
            self.answer_message(message, BotSystemMessages.KC_CLEARED)
        else:
            self.answer_message(message, BotSystemMessages.OPERATION_CANCELLED)

    def do_chat_message(self, message):
        if self.group_chat_id is not None:
            message_text = self.extract_text(message)
            self.send_message(
                self.group_chat_id,
                message_text)

    def _send_alert(self, message_text):
        if self.group_chat_id is not None:
            usernames = self.get_usernames(config.field_ids)
            alert_captions = ['@%s ' % username
                              for username in usernames.values()
                              if username is not None]
            alert_caption = ''.join(alert_captions) + '\r\n'
            self.send_message(
                self.group_chat_id,
                alert_caption + message_text,
                parse_mode="HTML")

    def do_alert(self, message):
        message_text = self.extract_text(message)
        self._send_alert(message_text)

    def do_message(self, message):
        message_text = self.extract_text(message)
        if len(message_text.split()) > 1:
            if message_text.split()[0].isdigit():
                user_id = int(message_text.split()[0])
                message_text = message_text.replace(message_text.split()[0], '').lstrip()
                self.send_message(
                    user_id,
                    message_text)
            else:
                self.answer_message(message,
                                    UserMessages.WRONG_USER_ID)
        else:
            self.answer_message(message,
                                CommandMessages.NO_MESSAGE)

    def do_message_admin(self, message):
        message_text = self.extract_text(message)
        for admin_id in config.admin_ids:
            self.send_message(admin_id,
                              message_text)

    def do_message_field(self, message):
        message_text = self.extract_text(message)
        for field_id in config.field_ids:
            self.send_message(field_id,
                              message_text)

    def do_message_kc(self, message):
        message_text = self.extract_text(message)
        for kc_id in config.kc_ids:
            self.send_message(kc_id,
                              message_text)

    def do_send_source(self, message):
        from_id = message["from_id"]
        source = self.game_worker.game_page
        if source is not None:
            self.send_file(from_id,
                           source,
                           'source.htm')
        else:
            self.answer_message(message,
                                FileMessages.NO_DATA_TO_DISPLAY)

    def do_send_errors(self, message):
        from_id = message["from_id"]
        if len(config.errors):
            self.send_file(from_id,
                           str(config.repr_errors()),
                           'errors.txt')
        else:
            self.answer_message(message,
                                FileMessages.NO_DATA_TO_DISPLAY)

    def do_clean_errors(self, message):
        config.clean_errors()
        self.answer_message(message,
                            BotSystemMessages.ERRORS_CLEARED)

    def do_token(self, message):
        new_token = self.get_new_value(message,
                                       BotSystemMessages.NEW_TOKEN.format(token=config.bot_token))
        if new_token != "NO":
            if config.bot_token != new_token:
                config.bot_token = new_token
                self._reset()
            from_id = message["from_id"]
            self.send_message(from_id, BotSystemMessages.TOKEN_CHANGED)
        else:
            self.answer_message(message, BotSystemMessages.TOKEN_CANCELLED)

    def do_codes_limit(self, message):
        codes_limit = self.get_new_value(message, BotSystemMessages.CODE_LIMIT)
        if codes_limit != "NO":
            if codes_limit.isdigit():
                config.code_limit = int(codes_limit)
                self.answer_message(message, BotSystemMessages.CODE_LIMIT_CHANGED)
            else:
                self.answer_message(message, BotSystemMessages.CODE_LIMIT_CANCELLED)
        else:
            self.answer_message(message, BotSystemMessages.CODE_LIMIT_CANCELLED)

    def do_change_login(self, message):
        new_login = self.get_new_value(message,
                                       SettingsMessages.GIVE_ME_NEW_LOGIN.format(login=config.game_login))
        if new_login != "NO":
            config.game_login = new_login
            GameDriver.login = config.game_login
            self.apply_new_settings(message)
        else:
            self.answer_message(message, SettingsMessages.SETTINGS_WERE_NOT_CHANGED)

    def do_change_pass(self, message):
        new_pass = self.get_new_value(message,
                                      SettingsMessages.GIVE_ME_NEW_PASSWORD.format(password=config.game_password))
        if new_pass != "NO":
            config.game_password = new_pass
            GameDriver.password = config.game_password
            self.apply_new_settings(message)
        else:
            self.answer_message(message, SettingsMessages.SETTINGS_WERE_NOT_CHANGED)

    def do_change_host(self, message):
        new_host = self.get_new_value(message,
                                      SettingsMessages.GIVE_ME_NEW_HOST.format(host=config.game_host))
        if new_host != "NO":
            config.game_host = new_host
            GameDriver.host = config.game_host
            self.apply_new_settings(message)
        else:
            self.answer_message(message, SettingsMessages.SETTINGS_WERE_NOT_CHANGED)

    def do_change_game(self, message):
        new_game = self.get_new_value(message,
                                      SettingsMessages.GIVE_ME_NEW_GAME.format(game=config.game_id))
        if new_game != "NO":
            if new_game.isdigit():
                config.game_id = int(new_game)
                GameDriver.game_id = config.game_id
                self.apply_new_settings(message)
            else:
                self.answer_message(message, SettingsMessages.SETTINGS_WERE_NOT_CHANGED)
        else:
            self.answer_message(message, SettingsMessages.SETTINGS_WERE_NOT_CHANGED)

    def do_set_tag_field(self, message):
        tag_field = self.get_new_value(message,
                                       SettingsMessages.TAG_FIELD)
        if tag_field == "NO":
            config.tag_field = False
        elif tag_field == "YES":
            config.tag_field = True
        else:
            self.answer_message(message, SettingsMessages.SETTINGS_WERE_NOT_CHANGED)
            return
        self.answer_message(message, SettingsMessages.SETTINGS_WERE_CHANGED)

    def do_set_autohandbrake(self, message):
        autohandbrake = self.get_new_value(message,
                                           SettingsMessages.AUTOHANDBRAKE)
        if autohandbrake == "ON":
            config.autohandbrake = True
        elif autohandbrake == "OFF":
            config.autohandbrake = False
        else:
            self.answer_message(message, SettingsMessages.SETTINGS_WERE_NOT_CHANGED)
            return
        self.answer_message(message, SettingsMessages.SETTINGS_WERE_CHANGED)

    def do_set_handbrake(self, message):
        handbrake = self.get_new_value(message,
                                       SettingsMessages.HANDBRAKE)
        if handbrake == "ON":
            self.game_worker.game_driver.handbrake = True
            self.game_worker.game_driver.auto_handbrake = True
        elif handbrake == "OFF":
            self.game_worker.game_driver.handbrake = False
            self.game_worker.game_driver.auto_handbrake = False
        else:
            self.answer_message(message, SettingsMessages.SETTINGS_WERE_NOT_CHANGED)
            return
        self.answer_message(message, SettingsMessages.SETTINGS_WERE_CHANGED)

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
            self.send_file(from_id,
                           unknown_message,
                           'unknown.txt')
        else:
            self.answer_message(message,
                                FileMessages.NO_DATA_TO_DISPLAY)

    def do_clean_unknown(self, message):
        self.unknown_users = []
        self.answer_message(message,
                            BotSystemMessages.UNKNOWN_CLEARED)

    def do_clean_memory(self, message):
        self.answer_message(message, BotSystemMessages.CONFIRM_DELETEION)
        answer = self.wait_for_answer(message["from_id"])
        if answer["text"] == "YES":
            self.game_worker.game_driver.codes_entered = {}
            self.game_worker.tasks_received = {}
            self.answer_message(message, BotSystemMessages.MEMORY_CLEARED)
        else:
            self.answer_message(message, BotSystemMessages.OPERATION_CANCELLED)

    def _do_disapprove(self, message):
        self.group_chat_id = None
        config.group_chat_id = self.group_chat_id
        self.paused = True
        config.paused = self.paused
        self.answer_message(message, CommonMessages.DISAPPROVE)

    def disapprove_command(self, message):
        from_id = message["from_id"]
        chat_id = message["chat_id"]
        if config.is_admin(from_id):
            if chat_id < 0:
                if chat_id == self.group_chat_id:
                    self._do_disapprove(message)
                else:
                    self.answer_message(message, CommonMessages.NO_GROUP_CHAT_MESSAGES)
            else:
                self.answer_message(message, CommonMessages.NOT_GROUP_CHAT)
        elif config.answer_forbidden:
            self.answer_message(message, CommonMessages.ACCESS_VIOLATION_MESSAGES)

    def do_status(self, message):
        hints_shown = ''
        for i in self.game_worker.hints_shown:
            hints_shown += str(i) + ' '
        status_message = HelpMessages.STATUS.format(
            paused=HelpMessages.PAUSED[self.paused],
            chat_id=self.group_chat_id,
            game_connection=HelpMessages.GAME_CONNECTION[self.game_worker.game_driver.is_logged()],
            game_level_id=self.game_worker.last_level_shown,
            game_hint_id=hints_shown,
            handbrake=str(self.game_worker.game_driver.handbrake or self.game_worker.game_driver.auto_handbrake),
            codes_limit=config.code_limit
        )
        self.answer_message(message, status_message)

    def do_info(self, message):
        info_message = HelpMessages.INFO.format(
            chat_id=self.group_chat_id,
            login=self.game_worker.game_driver.login,
            password=self.game_worker.game_driver.password,
            host=self.game_worker.game_driver.host,
            game_id=self.game_worker.game_driver.game_id,
            admins=json.dumps(self.get_usernames(config.admin_ids)),
            fields=json.dumps(self.get_usernames(config.field_ids)),
            kcs=json.dumps(self.get_usernames(config.kc_ids)),
            admin_passphrase=config.admin_passphrase,
            field_passphrase=config.field_passphrase,
            kc_passphrase=config.kc_passphrase,
            time_start=config.start_time,
            bot_errors=len(config.errors),
            token=config.bot_token,
            rnd=self.game_worker.game_driver.rnd,
            codelimit=config.code_limit,
            unknown_users=len(self.unknown_users),
            tag_field=str(config.tag_field),
            autohandbrake=str(config.autohandbrake))
        self.answer_message(message, info_message, parse_mode="HTML")

    def do_reset(self, message):
        self.game_worker.reset_level()
        self.answer_message(message, BotSystemMessages.BOT_WAS_RESET)

    def do_task(self, message):
        if len(message["text"].split()) > 1:
            level_to_show = int(message["text"].split()[1])
            task_source = self.game_worker.tasks_received.get(level_to_show)
            if task_source is not None:
                task_text = self.game_worker.game_driver.get_task(task_source)
                task_text = GameMessages.TASK_MESSAGE.format(
                    level_number=level_to_show,
                    task=task_text)
            else:
                task_text = CommandMessages.WRONG_LEVEL_ID
        else:
            task_text = GameMessages.TASK_MESSAGE.format(
                level_number=self.game_worker.last_level_shown,
                task=self.game_worker.last_task_text)
        self.answer_message(message, task_text, parse_mode="HTML")

    def do_tasks_all(self, message):
        all_tasks = ""
        if message["chat_id"] == self.group_chat_id:
            from_id = message["chat_id"]
        else:
            from_id = message["from_id"]
        for level_number, task in self.game_worker.tasks_received.iteritems():
            task_text = self.game_worker.game_driver.get_task(task)
            all_tasks += u"{level_number}:\r\n\r\n{task}\r\n".format(level_number=level_number, task=task_text)
        if len(all_tasks):
            self.send_file(from_id, all_tasks, "all_tasks.txt")
        else:
            self.answer_message(message, CommandMessages.NO_TASKS_RECEIVED)

    def do_task_html(self, message):
        if message["chat_id"] == self.group_chat_id:
            from_id = message["chat_id"]
        else:
            from_id = message["from_id"]
        if len(message["text"].split()) > 1:
            level_to_show = int(message["text"].split()[1])
            task_text = self.game_worker.tasks_received.get(level_to_show)
            if task_text is not None:
                self.send_file(from_id, task_text, "task_%s.html" % level_to_show)
            else:
                self.answer_message(message, CommandMessages.WRONG_LEVEL_ID)
        else:
            if self.game_worker.last_level_shown is not None:
                task_text = self.game_worker.tasks_received.get(self.game_worker.last_level_shown)
                self.send_file(from_id, task_text, "task_%s.html" % self.game_worker.last_level_shown)
            else:
                self.answer_message(message, CommandMessages.NO_TASKS_RECEIVED)

    def do_codes_history(self, message):
        if len(message["text"].split()) > 1:
            level_to_show = int(message["text"].split()[1])
            codes_entered = self.game_worker.game_driver.codes_entered.get(level_to_show)
            if codes_entered is not None:
                all_codes = ""
                for username, user_codes in codes_entered.iteritems():
                    if username != "__all__":
                        codes_template = u"<b>{username}</b>: {codes}\r\n"
                        user_codes_formatted = ' '.join(user_codes)
                        all_codes += codes_template.format(username=username,
                                                           codes=user_codes_formatted)
            else:
                all_codes = CommandMessages.WRONG_LEVEL_ID
            self.answer_message(message, all_codes, parse_mode="HTML")
        else:
            self.answer_message(message, CommandMessages.NO_TASK_ID)

    def do_codes_all(self, message):
        all_codes = ""
        if message["chat_id"] == self.group_chat_id:
            from_id = message["chat_id"]
        else:
            from_id = message["from_id"]
        for level, codes in self.game_worker.game_driver.codes_entered.iteritems():
            all_codes += "---------\r\n{level}:\r\n---------\r\n\r\n".format(level=level)
            for username, user_codes in codes.iteritems():
                if username != "__all__":
                    codes_template = u"{username}: {codes}\r\n"
                    user_codes_formatted = ' '.join(user_codes)
                    all_codes += codes_template.format(username=username,
                                                       codes=user_codes_formatted)
        if len(all_codes):
            self.send_file(from_id, all_codes, "all_codes.txt")
        else:
            self.answer_message(message, CommandMessages.NO_CODES_ENTERED)

    def do_hints(self, message):
        hints = []
        for hint_id in sorted(self.game_worker.all_hints.keys()):
            hints.append(GameMessages.NEW_HINT.format(
                smile=Smiles.HINTS,
                hint_number=hint_id,
                hint=self.game_worker.all_hints[hint_id]))
        for hint in hints:
            self.answer_message(message, hint, parse_mode="HTML")
        else:
            self.answer_message(message, GameMessages.NO_HINTS, parse_mode="HTML")

    def do_help(self, message):
        from_id = message["from_id"]
        if config.is_admin(from_id):
            self.answer_message(message, HelpMessages.ADMIN_HELP)
        else:
            self.answer_message(message, HelpMessages.REGULAR_HELP)

    def do_gap(self, message):
        codes_gap = self.game_worker.game_driver.get_codes_gap()
        self.answer_message(message,
                            codes_gap)

    def apply_new_settings(self, message):
        self.game_worker = GameWorker()
        self.paused = True
        config.paused = self.paused
        self.admin_message(SettingsMessages.SETTINGS_WERE_CHANGED)
        if self.game_worker.connected:
            self.admin_message(CommonMessages.CONNECTION_OK_MESSAGES)
            self.admin_message(CommonMessages.PLEASE_APPROVE_MESSAGES)
            self.do_reset(message)
            self.paused = False
            config.paused = self.paused
            return True
        else:
            self.admin_message(SettingsMessages.CONNECTION_PROBLEM)
            self.admin_message(SettingsMessages.CHECK_SETTINGS)
            return False

    def do_edit_settings(self, message):
        from_id = message["from_id"]

        self.send_message(
            from_id,
            SettingsMessages.GIVE_ME_LOGIN)
        GameDriver.login = self.wait_for_answer(from_id)["text"]
        config.game_login = GameDriver.login
        self.send_message(
            from_id,
            SettingsMessages.GIVE_ME_PASSWORD)
        GameDriver.password = self.wait_for_answer(from_id)["text"]
        config.game_password = GameDriver.password
        self.send_message(
            from_id,
            SettingsMessages.GIVE_ME_HOST)
        GameDriver.host = self.wait_for_answer(from_id)["text"]
        config.game_host = GameDriver.host
        self.send_message(
            from_id,
            SettingsMessages.GIVE_ME_GAME)
        GameDriver.game_id = self.wait_for_answer(from_id)["text"]
        config.game_id = GameDriver.game_id

        self.apply_new_settings(message)

    def do_save_settings(self, message):
        result = config.save_config()
        if result:
            self.answer_message(message, SettingsMessages.SETTINGS_WERE_SAVED)
        else:
            self.answer_message(message, SettingsMessages.SETTINGS_WERE_NOT_SAVED)

    def unknown_command(self, message):
        if config.answer_unknown:
            self.answer_message(message, CommonMessages.UNKNOWN)

    def process_unknown_user(self, message):
        from_id = message["from_id"]
        if from_id not in config.admin_ids + config.field_ids + config.kc_ids:
            self.unknown_users.append({"timestamp": datetime.datetime.now(),
                                       "user_id": from_id,
                                       "username": message["username"],
                                       "message_text": message["text"]})
            if len(self.unknown_users) >= 100:
                self.unknown_users[from_id].pop(0)
            return True
        else:
            return False

    def process_new_user(self, message):
        passphrase = message["text"]
        from_id = message["from_id"]
        if passphrase == config.admin_passphrase:
            if from_id in config.admin_ids:
                return False
            else:
                config.add_admin_id(int(from_id))
                self.answer_message(message, UserMessages.HELLO_NEW_ADMIN)
                self.admin_message(
                    UserMessages.NEW_ADMIN_WAS_ADDED.format(user_id=from_id,
                                                            nickname=self.get_username(from_id)))
                return True
        elif passphrase == config.field_passphrase:
            if from_id in config.field_ids:
                return False
            else:
                config.add_field_id(int(from_id))
                self.answer_message(message, UserMessages.HELLO_NEW_USER)
                self.admin_message(
                    UserMessages.NEW_FIELD_WAS_ADDED.format(user_id=from_id,
                                                            nickname=self.get_username(from_id)))
                return True
        elif passphrase == config.kc_passphrase:
            if from_id in config.kc_ids:
                return False
            else:
                config.add_kc_id(int(from_id))
                self.answer_message(message, UserMessages.HELLO_NEW_USER)
                self.admin_message(
                    UserMessages.NEW_KC_WAS_ADDED.format(user_id=from_id,
                                                         nickname=self.get_username(from_id)))
                return True
        else:
            return False

    def dublicate_code_to_group_chat(self, message, result):
        from_id = message["from_id"]
        if config.is_field(from_id) \
                and self.group_chat_id is not None \
                and message["chat_id"] != self.group_chat_id \
                and result is not None:
            self.send_message(
                self.group_chat_id,
                CommandMessages.FIELD_TRIED_CODE.format(
                    nickname=self.get_username(from_id),
                    codes=result),
                parse_mode="HTML")

    def process_code_simple_message(self, message):
        from_id = message["from_id"]
        if from_id in config.field_ids:
            if not message['text'].startswith('/'):
                if not self.paused:
                    result = self.check_code(message)
                    self.answer_message(message, result)
                    self.dublicate_code_to_group_chat(message, result)
                else:
                    self.answer_message(message, CommonMessages.PAUSED)
        elif from_id in config.kc_ids:
            if not message['text'].startswith('/'):
                if not self.paused:
                    result = self.check_code(message)
                    self.answer_message(message, result)
                else:
                    self.answer_message(message, CommonMessages.PAUSED)
