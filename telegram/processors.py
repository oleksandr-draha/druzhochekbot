# -*- coding: utf-8 -*-
import json

from config import bot_settings, errors_log, game_settings, unknown_log, codes_log, tasks_log, timeouts
from config.dictionary import Smiles, CommonMessages, BotSystemMessages, CommandMessages, SettingsMessages, \
    UserMessages, GameMessages, FileMessages, HelpMessages
from game.worker import GameWorker
from telegram.abstract_processors import AbstractProcessors
from telegram.codes import CodesQueue


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
                              GameMessages.GAME_NOT_APPROVED,
                              GameMessages.GAME_NOT_STARTED,
                              GameMessages.BANNED,
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
        if not bot_settings.paused:
            self.answer_message(message, CommonMessages.DO_PAUSE)
            bot_settings.paused = True
        else:
            self.answer_message(message, CommonMessages.ALREADY_PAUSED)

    def do_resume(self, message):
        if bot_settings.paused:
            self.answer_message(message, CommonMessages.DO_RESUME)
            bot_settings.paused = False
        else:
            self.answer_message(message, CommonMessages.ALREADY_WORKING)

    def do_codes(self, message):
        if not bot_settings.paused:
            if len(message["text"].split()) > 1:
                CodesQueue.add_code_bunch(message, split=True)
                # result = self.check_codes(message)
                # self.answer_message(message, result, parse_mode="html")
                # self.duplicate_code_to_group_chat(message, result)
            else:
                self.answer_message(message, CommandMessages.NO_CODE_FOUND)
        else:
            self.answer_message(message, CommonMessages.PAUSED)

    def do_code(self, message):
        if not bot_settings.paused:
            if len(message["text"].split()) > 1:
                CodesQueue.add_code_bunch(message)
                # result = self.check_code(message)
                # self.answer_message(message, result, parse_mode="html")
                # self.duplicate_code_to_group_chat(message, result)
            else:
                self.answer_message(message, CommandMessages.NO_CODE_FOUND)
        else:
            self.answer_message(message, CommonMessages.PAUSED)

    def _do_approve(self, message):
        chat_id = message["chat_id"]
        title = message["title"]
        self.answer_message(message, CommonMessages.LETS_GO)
        bot_settings.group_chat_id = chat_id
        bot_settings.group_chat_name = title
        bot_settings.paused = False

    def approve_command(self, message):
        from_id = message["from_id"]
        chat_id = message["chat_id"]
        if bot_settings.is_admin(from_id):
            if chat_id < 0:
                self._do_approve(message)
            else:
                self.answer_message(message, CommonMessages.NOT_GROUP_CHAT)
        elif bot_settings.answer_forbidden:
            self.answer_message(message, CommonMessages.ACCESS_VIOLATION_MESSAGES)

    def do_add_admin(self, message):
        if len(message["text"].split()) > 1:
            admin_to_add = message["text"].split()[1]
            if not admin_to_add.isdigit():
                self.answer_message(message, UserMessages.WRONG_USER_ID)
            else:
                if bot_settings.is_admin(int(admin_to_add)):
                    self.answer_message(
                        message,
                        UserMessages.DUPLICATE_USER_ID)
                else:
                    bot_settings.add_admin_id(int(admin_to_add))
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
                bot_settings.group_chat_id = int(group_chat_id)
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
                if bot_settings.is_field(int(field_to_add)):
                    self.answer_message(
                        message,
                        UserMessages.DUPLICATE_USER_ID)
                else:
                    bot_settings.add_field_id(int(field_to_add))
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
                if bot_settings.is_kc(int(kc_to_add)):
                    self.answer_message(
                        message,
                        UserMessages.DUPLICATE_USER_ID)
                else:
                    bot_settings.add_kc_id(int(kc_to_add))
                    self.admin_message(
                        UserMessages.NEW_KC_WAS_ADDED.format(
                            user_id=kc_to_add,
                            nickname=self.get_username(kc_to_add)))
                    self.send_message(kc_to_add, UserMessages.HELLO_NEW_USER)
        else:
            self.answer_message(message,
                                CommandMessages.NO_USER_ID)

    def do_delete_admin(self, message):
        if len(bot_settings.admin_ids) == 1:
            self.answer_message(message, UserMessages.CANNOT_DELETE_ADMIN)
        else:
            admin_to_delete = self.get_new_value(
                message,
                UserMessages.DELETE_USER_ID.format(
                    current_ids=self.get_usernames(bot_settings.admin_ids)))
            if not admin_to_delete.isdigit() or int(admin_to_delete) not in bot_settings.admin_ids:
                self.answer_message(message, UserMessages.WRONG_USER_ID)
            else:
                bot_settings.delete_admin_id(int(admin_to_delete))
                self.answer_message(message, UserMessages.USER_DELETED)

    def do_delete_field(self, message):
        field_to_delete = self.get_new_value(
            message,
            UserMessages.DELETE_USER_ID.format(
                current_ids=self.get_usernames(bot_settings.field_ids)))
        if not field_to_delete.isdigit() or int(field_to_delete) not in bot_settings.field_ids:
            self.answer_message(message, UserMessages.WRONG_USER_ID)
        else:
            bot_settings.delete_field_id(int(field_to_delete))
            self.answer_message(message, UserMessages.USER_DELETED)

    def do_delete_kc(self, message):
        kc_to_delete = self.get_new_value(
            message,
            UserMessages.DELETE_USER_ID.format(
                current_ids=self.get_usernames(bot_settings.kc_ids)))
        if not kc_to_delete.isdigit() or int(kc_to_delete) not in bot_settings.kc_ids:
            self.answer_message(message, UserMessages.WRONG_USER_ID)
        else:
            bot_settings.delete_kc_id(int(kc_to_delete))
            self.answer_message(message, UserMessages.USER_DELETED)

    def do_edit_admin_pass(self, message):
        new = self.get_new_value(
            message,
            SettingsMessages.ENTER_NEW_PASS.format(code=bot_settings.admin_passphrase))
        old = bot_settings.admin_passphrase
        if new not in bot_settings.passphrases:
            bot_settings.admin_passphrase = new
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
            SettingsMessages.ENTER_NEW_PASS.format(code=bot_settings.field_passphrase))
        old = bot_settings.field_passphrase
        if new not in bot_settings.passphrases:
            bot_settings.field_passphrase = new
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
            SettingsMessages.ENTER_NEW_PASS.format(code=bot_settings.kc_passphrase))
        old = bot_settings.kc_passphrase
        if new not in bot_settings.passphrases:
            bot_settings.kc_passphrase = new
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
            bot_settings.clean_admins()
            self.answer_message(message, BotSystemMessages.ADMIN_CLEARED)
        else:
            self.answer_message(message, BotSystemMessages.OPERATION_CANCELLED)

    def do_cleanfield(self, message):
        self.answer_message(message, BotSystemMessages.CONFIRM_DELETEION)
        answer = self.wait_for_answer(message["from_id"])
        if answer["text"] == "YES":
            bot_settings.clean_fields()
            self.answer_message(message, BotSystemMessages.FIELD_CLEARED)
        else:
            self.answer_message(message, BotSystemMessages.OPERATION_CANCELLED)

    def do_cleankc(self, message):
        self.answer_message(message, BotSystemMessages.CONFIRM_DELETEION)
        answer = self.wait_for_answer(message["from_id"])
        if answer["text"] == "YES":
            bot_settings.clean_kcs()
            self.answer_message(message, BotSystemMessages.KC_CLEARED)
        else:
            self.answer_message(message, BotSystemMessages.OPERATION_CANCELLED)

    def do_chat_message(self, message):
        if bot_settings.group_chat_id is not None:
            message_text = self.extract_text(message)
            self.send_message(
                bot_settings.group_chat_id,
                message_text)

    def get_alert_captions(self):
        usernames = self.get_usernames(bot_settings.field_ids)
        alert_captions = ['@%s ' % username
                          for username in usernames.values()
                          if username is not None]
        alert_caption = '\r\n\r\n' + "".join(alert_captions) + '\r\n'
        return alert_caption

    def _send_alert(self, message_text):
        if bot_settings.group_chat_id is not None:
            alert_caption = self.get_alert_captions()
            self.send_message(
                bot_settings.group_chat_id,
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
        for admin_id in bot_settings.admin_ids:
            self.send_message(admin_id,
                              message_text)

    def do_message_field(self, message):
        message_text = self.extract_text(message)
        for field_id in bot_settings.field_ids:
            self.send_message(field_id,
                              message_text)

    def do_message_kc(self, message):
        message_text = self.extract_text(message)
        for kc_id in bot_settings.kc_ids:
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

    def do_show_codes_queue(self, message):
        from_id = message["from_id"]
        if CodesQueue.pending:
            self.send_file(from_id,
                           json.dumps(CodesQueue.codes_queue_repr()),
                           'codes.txt')
        else:
            self.answer_message(message,
                                FileMessages.NO_DATA_TO_DISPLAY)

    def do_show_codes_queue_statistic(self, message):
        if CodesQueue.pending:
            self.answer_message(message,
                                CodesQueue.codes_queue_statistic_repr())
        else:
            self.answer_message(message,
                                FileMessages.NO_DATA_TO_DISPLAY)

    def do_send_errors(self, message):
        from_id = message["from_id"]
        if len(errors_log.errors_raw):
            self.send_file(from_id,
                           str(errors_log.repr_errors()),
                           'errors.txt')
        else:
            self.answer_message(message,
                                FileMessages.NO_DATA_TO_DISPLAY)

    def do_clean_errors(self, message):
        errors_log.clean_errors()
        self.answer_message(message,
                            BotSystemMessages.ERRORS_CLEARED)

    def do_token(self, message):
        new_token = self.get_new_value(message,
                                       BotSystemMessages.NEW_TOKEN.format(token=bot_settings.bot_token))
        if new_token != "NO":
            if bot_settings.bot_token != new_token:
                bot_settings.bot_token = new_token
                self._reset()
            from_id = message["from_id"]
            self.send_message(from_id, BotSystemMessages.TOKEN_CHANGED)
        else:
            self.answer_message(message, BotSystemMessages.TOKEN_CANCELLED)

    def do_codes_interval(self, message):
        codes_interval = self.get_new_value(message, BotSystemMessages.CODE_INTERVAL)
        if codes_interval != "NO":
            if codes_interval.isdigit():
                timeouts.codes_interval = int(codes_interval)
                self.answer_message(message, BotSystemMessages.CODE_INTERVAL_CHANGED)
            else:
                self.answer_message(message, BotSystemMessages.CODE_INTERVAL_CANCELLED)
        else:
            self.answer_message(message, BotSystemMessages.CODE_INTERVAL_CANCELLED)

    def do_change_login(self, message):
        new_login = self.get_new_value(message,
                                       SettingsMessages.GIVE_ME_NEW_LOGIN.format(login=game_settings.game_login))
        if new_login != "NO":
            game_settings.game_login = new_login
            self.apply_new_settings(message)
        else:
            self.answer_message(message, SettingsMessages.SETTINGS_WERE_NOT_CHANGED)

    def do_change_pass(self, message):
        new_pass = self.get_new_value(message,
                                      SettingsMessages.GIVE_ME_NEW_PASSWORD.format(password=game_settings.game_password))
        if new_pass != "NO":
            game_settings.game_password = new_pass
            self.apply_new_settings(message)
        else:
            self.answer_message(message, SettingsMessages.SETTINGS_WERE_NOT_CHANGED)

    def do_change_host(self, message):
        new_host = self.get_new_value(message,
                                      SettingsMessages.GIVE_ME_NEW_HOST.format(host=game_settings.game_host))
        if new_host != "NO":
            game_settings.game_host = new_host
            self.apply_new_settings(message)
        else:
            self.answer_message(message, SettingsMessages.SETTINGS_WERE_NOT_CHANGED)

    def do_change_game(self, message):
        new_game = self.get_new_value(message,
                                      SettingsMessages.GIVE_ME_NEW_GAME.format(game=game_settings.game_id))
        if new_game != "NO":
            if new_game.isdigit():
                game_settings.game_id = int(new_game)
                self.apply_new_settings(message)
            else:
                self.answer_message(message, SettingsMessages.SETTINGS_WERE_NOT_CHANGED)
        else:
            self.answer_message(message, SettingsMessages.SETTINGS_WERE_NOT_CHANGED)

    def do_set_tag_field(self, message):
        tag_field = self.get_new_value(message,
                                       SettingsMessages.TAG_FIELD)
        if tag_field == "NO":
            bot_settings.tag_field = False
        elif tag_field == "YES":
            bot_settings.tag_field = True
        else:
            self.answer_message(message, SettingsMessages.SETTINGS_WERE_NOT_CHANGED)
            return
        self.answer_message(message, SettingsMessages.SETTINGS_WERE_CHANGED)

    def do_set_send_task_to_private(self, message):
        send_task_to_private = self.get_new_value(message,
                                                  SettingsMessages.SEND_TASK_TO_PRIVATE_FIELD)
        if send_task_to_private == "NO":
            bot_settings.send_task_to_private = False
        elif send_task_to_private == "YES":
            bot_settings.send_task_to_private = True
        else:
            self.answer_message(message, SettingsMessages.SETTINGS_WERE_NOT_CHANGED)
            return
        self.answer_message(message, SettingsMessages.SETTINGS_WERE_CHANGED)

    def do_set_log_activity(self, message):
        tag_field = self.get_new_value(message,
                                       SettingsMessages.LOG_ACTIVITY)
        if tag_field == "NO":
            bot_settings.log_activity = False
        elif tag_field == "YES":
            bot_settings.log_activity = True
        else:
            self.answer_message(message, SettingsMessages.SETTINGS_WERE_NOT_CHANGED)
            return
        self.answer_message(message, SettingsMessages.SETTINGS_WERE_CHANGED)

    def do_clean_codes_queue(self, message):
        self.answer_message(message, BotSystemMessages.CONFIRM_DELETEION)
        answer = self.wait_for_answer(message["from_id"])
        if answer["text"] == "YES":
            CodesQueue.reset()
            self.answer_message(message, BotSystemMessages.CODES_QUEUE_CLEARED)
        else:
            self.answer_message(message, BotSystemMessages.OPERATION_CANCELLED)

    def do_stop_codes_queue(self, message):
        self.answer_message(message, BotSystemMessages.CONFIRM_DELETEION)
        answer = self.wait_for_answer(message["from_id"])
        if answer["text"] == "YES":
            CodesQueue.soft_reset()
            self.answer_message(message, BotSystemMessages.CODES_QUEUE_CLEARED)
        else:
            self.answer_message(message, BotSystemMessages.OPERATION_CANCELLED)

    def do_set_autohandbrake(self, message):
        autohandbrake = self.get_new_value(message,
                                           SettingsMessages.AUTOHANDBRAKE)
        if autohandbrake == "ON":
            bot_settings.autohandbrake = True
        elif autohandbrake == "OFF":
            bot_settings.autohandbrake = False
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
        unknown_message = unknown_log.repr_unknown()
        if len(unknown_message):
            self.send_file(from_id,
                           unknown_message,
                           'unknown.txt')
        else:
            self.answer_message(message,
                                FileMessages.NO_DATA_TO_DISPLAY)

    def do_clean_unknown(self, message):
        unknown_log.unknown_raw = []
        self.answer_message(message,
                            BotSystemMessages.UNKNOWN_CLEARED)

    def do_clean_memory(self, message):
        self.answer_message(message, BotSystemMessages.CONFIRM_DELETEION)
        answer = self.wait_for_answer(message["from_id"])
        if answer["text"] == "YES":
            codes_log.clean_codes()
            tasks_log.clean_tasks()
            self.answer_message(message, BotSystemMessages.MEMORY_CLEARED)
        else:
            self.answer_message(message, BotSystemMessages.OPERATION_CANCELLED)

    def _do_disapprove(self, message):
        bot_settings.group_chat_id = None
        bot_settings.group_chat_name = None
        bot_settings.paused = True
        self.answer_message(message, CommonMessages.DISAPPROVE)

    def disapprove_command(self, message):
        from_id = message["from_id"]
        chat_id = message["chat_id"]
        if bot_settings.is_admin(from_id):
            if chat_id < 0:
                if chat_id == bot_settings.group_chat_id:
                    self._do_disapprove(message)
                else:
                    self.answer_message(message, CommonMessages.NO_GROUP_CHAT_MESSAGES)
            else:
                self.answer_message(message, CommonMessages.NOT_GROUP_CHAT)
        elif bot_settings.answer_forbidden:
            self.answer_message(message, CommonMessages.ACCESS_VIOLATION_MESSAGES)

    def do_status(self, message):
        hints_shown = ''
        for i in self.game_worker.hints_shown:
            hints_shown += str(i) + ' '
        status_message = HelpMessages.STATUS.format(
            paused=HelpMessages.PAUSED[bot_settings.paused],
            chat_id=bot_settings.group_chat_id,
            chat_group_name=bot_settings.group_chat_name,
            game_connection=HelpMessages.GAME_CONNECTION[self.game_worker.game_driver.is_logged()],
            game_level_id=self.game_worker.last_level_shown,
            game_hint_id=hints_shown,
            handbrake=str(self.game_worker.game_driver.handbrake or self.game_worker.game_driver.auto_handbrake),
            codes_interval=timeouts.codes_interval
        )
        self.answer_message(message, status_message)

    def do_info(self, message):
        info_message = HelpMessages.INFO.format(
            chat_id=bot_settings.group_chat_id,
            login=game_settings.game_login,
            password=game_settings.game_password,
            host=game_settings.game_host,
            game_id=game_settings.game_id,
            admins=json.dumps(self.get_usernames(bot_settings.admin_ids)),
            fields=json.dumps(self.get_usernames(bot_settings.field_ids)),
            kcs=json.dumps(self.get_usernames(bot_settings.kc_ids)),
            admin_passphrase=bot_settings.admin_passphrase,
            field_passphrase=bot_settings.field_passphrase,
            kc_passphrase=bot_settings.kc_passphrase,
            time_start=bot_settings.start_time,
            bot_errors=len(errors_log.errors_raw),
            token=bot_settings.bot_token,
            rnd=self.game_worker.game_driver.rnd,
            codes_interval=timeouts.codes_interval,
            unknown_users=len(unknown_log.unknown_raw),
            tag_field=str(bot_settings.tag_field),
            send_task_to_private=str(bot_settings.send_task_to_private),
            autohandbrake=str(bot_settings.autohandbrake),
            log_activity=str(bot_settings.log_activity))
        self.answer_message(message, info_message, parse_mode="HTML")

    def do_reset(self, message):
        self.game_worker.reset_level()
        self.answer_message(message, BotSystemMessages.BOT_WAS_RESET)

    def do_task(self, message):
        if len(message["text"].split()) > 1:
            level_to_show = int(message["text"].split()[1])
            task_source = tasks_log.task(level_to_show)
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
        if message["chat_id"] == bot_settings.group_chat_id:
            from_id = message["chat_id"]
        else:
            from_id = message["from_id"]
        for level_number, task in tasks_log.tasks_raw.iteritems():
            task_text = self.game_worker.game_driver.get_task(task)
            all_tasks += u"{level_number}:" \
                         u"\r\n-------------------------------------" \
                         u"\r\n{task}\r\n-------------------------------------" \
                         u"\r\n".format(level_number=level_number, task=task_text)
        if len(all_tasks):
            self.send_file(from_id, all_tasks, "all_tasks.txt")
        else:
            self.answer_message(message, CommandMessages.NO_TASKS_RECEIVED)

    def do_task_html(self, message):
        if message["chat_id"] == bot_settings.group_chat_id:
            from_id = message["chat_id"]
        else:
            from_id = message["from_id"]
        if len(message["text"].split()) > 1:
            level_to_show = int(message["text"].split()[1])
            task_text = tasks_log.task(level_to_show)
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
            all_codes = codes_log.repr_codes_by_level(level_to_show)
            if not len(all_codes):
                all_codes = CommandMessages.WRONG_LEVEL_ID
            self.answer_message(message, all_codes, parse_mode="HTML")
        else:
            self.answer_message(message, CommandMessages.NO_TASK_ID)

    def do_codes_all(self, message):
        if message["chat_id"] == bot_settings.group_chat_id:
            from_id = message["chat_id"]
        else:
            from_id = message["from_id"]
        all_codes = codes_log.repr_codes_all()
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
        if len(hints):
            for hint in hints:
                self.answer_message(message, hint, parse_mode="HTML")
        else:
            self.answer_message(message, GameMessages.NO_HINTS, parse_mode="HTML")

    def do_help(self, message):
        from_id = message["from_id"]
        if bot_settings.is_admin(from_id):
            self.answer_message(message, HelpMessages.ADMIN_HELP)
        else:
            self.answer_message(message, HelpMessages.REGULAR_HELP)

    def do_gap(self, message):
        codes_gap = self.game_worker.game_driver.get_codes_gap()
        self.answer_message(message,
                            codes_gap)

    def do_codes_statistic(self, message):
        all = 0
        players = {}
        for level, codes in codes_log.codes_raw.iteritems():
            all += len(codes.get("__all__", 0))
            for username, cods in codes.iteritems():
                if username != "__all__":
                    num = players.get(username, 0) + len(cods)
                    players.update({username: num})
        statistic = "*Total*: {all}\r\n".format(all=all)
        for username, num in players.iteritems():
            statistic += "*{username}*: {num}\r\n".format(username=username, num=num)
        self.answer_message(message,
                            statistic)

    def apply_new_settings(self, message):
        self.game_worker = GameWorker()
        bot_settings.paused = True
        self.admin_message(SettingsMessages.SETTINGS_WERE_CHANGED)
        if self.game_worker.connected:
            self.admin_message(CommonMessages.CONNECTION_OK_MESSAGES)
            self.admin_message(CommonMessages.PLEASE_APPROVE_MESSAGES)
            self.do_reset(message)
            bot_settings.paused = False
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
        game_settings.game_login = self.wait_for_answer(from_id)["text"]
        self.send_message(
            from_id,
            SettingsMessages.GIVE_ME_PASSWORD)
        game_settings.game_password = self.wait_for_answer(from_id)["text"]
        self.send_message(
            from_id,
            SettingsMessages.GIVE_ME_HOST)
        game_settings.game_host = self.wait_for_answer(from_id)["text"]
        self.send_message(
            from_id,
            SettingsMessages.GIVE_ME_GAME)
        game_settings.game_id = self.wait_for_answer(from_id)["text"]

        self.apply_new_settings(message)

    def unknown_command(self, message):
        if bot_settings.answer_unknown:
            self.answer_message(message, CommonMessages.UNKNOWN)

    def process_unknown_user(self, message):
        from_id = message["from_id"]
        if not bot_settings.is_user(from_id):
            unknown_log.log_unknown(message)
            return True
        else:
            return False

    def process_new_user(self, message):
        passphrase = message["text"]
        from_id = message["from_id"]
        if passphrase == bot_settings.admin_passphrase:
            if from_id in bot_settings.admin_ids:
                return False
            else:
                bot_settings.add_admin_id(int(from_id))
                self.answer_message(message, UserMessages.HELLO_NEW_ADMIN)
                self.admin_message(
                    UserMessages.NEW_ADMIN_WAS_ADDED.format(user_id=from_id,
                                                            nickname=self.get_username(from_id)))
                return True
        elif passphrase == bot_settings.field_passphrase:
            if from_id in bot_settings.field_ids:
                return False
            else:
                bot_settings.add_field_id(int(from_id))
                self.answer_message(message, UserMessages.HELLO_NEW_USER)
                self.admin_message(
                    UserMessages.NEW_FIELD_WAS_ADDED.format(user_id=from_id,
                                                            nickname=self.get_username(from_id)))
                return True
        elif passphrase == bot_settings.kc_passphrase:
            if from_id in bot_settings.kc_ids:
                return False
            else:
                bot_settings.add_kc_id(int(from_id))
                self.answer_message(message, UserMessages.HELLO_NEW_USER)
                self.admin_message(
                    UserMessages.NEW_KC_WAS_ADDED.format(user_id=from_id,
                                                         nickname=self.get_username(from_id)))
                return True
        else:
            return False

    def duplicate_code_to_group_chat(self, message, result):
        from_id = message["from_id"]
        if bot_settings.is_field(from_id) \
                and bot_settings.group_chat_id is not None \
                and message["chat_id"] != bot_settings.group_chat_id \
                and result is not None:
            if result not in [GameMessages.CODES_BLOCKED,
                              GameMessages.GAME_FINISHED,
                              GameMessages.GAME_NOT_PAYED,
                              GameMessages.GAME_NOT_APPROVED,
                              GameMessages.GAME_NOT_STARTED,
                              GameMessages.BANNED,
                              GameMessages.HANDBRAKE]:
                self.send_message(
                    bot_settings.group_chat_id,
                    CommandMessages.FIELD_TRIED_CODE.format(
                        nickname=self.get_username(from_id),
                        codes=result),
                    parse_mode="HTML")

    def process_code_simple_message(self, message):
        from_id = message["from_id"]
        if from_id in bot_settings.field_ids:
            if not message['text'].startswith('/'):
                if not bot_settings.paused:
                    CodesQueue.add_code_bunch(message)
                    # result = self.check_code(message)
                    # self.answer_message(message, result)
                    # self.duplicate_code_to_group_chat(message, result)
                else:
                    self.answer_message(message, CommonMessages.PAUSED)
        elif from_id in bot_settings.kc_ids:
            if not message['text'].startswith('/'):
                if not bot_settings.paused:
                    CodesQueue.add_code_bunch(message)
                    # result = self.check_code(message)
                    # self.answer_message(message, result)
                else:
                    self.answer_message(message, CommonMessages.PAUSED)
