# -*- coding: utf-8 -*-
from random import randint

from requests import ConnectionError, session
import html2text

from config.dictionary import Smiles, GameMessages, CommandMessages
from config import game_settings, codes_log, timeouts
from game.locators import GameState, InGame


class GameDriver:
    level_id = None
    level_number = None
    connected = False
    codes_entered = {}
    rnd = "0,%s" % randint(100000000000000, 999999999999999)
    handbrake = False
    auto_handbrake = False

    def __init__(self):
        self.session = session()
        try:
            self.login_user()
            game_page = self.get_game_page()
            if self.is_logged(game_page):
                if self.game_active(game_page):
                    self.set_level_params(game_page)
                self.connected = True
            else:
                self.connected = False
        except ConnectionError:
            self.connected = False

    def login_user(self):
        try:
            body = {"Login": game_settings.game_login,
                    "Password": game_settings.game_password,
                    "SelectedNetworkId": 2}
            return self.session.post(game_settings.quest_url.format(
                host=game_settings.game_host,
                path=game_settings.quest_login_url),
                params=body).text
        except ConnectionError:
            return ''

    def is_logged(self, text=None):
        if text is None:
            text = self.get_game_page()
        return self.game_active(text) or self.game_inactive(text)

    def game_active(self, text=None):
        if text is None:
            text = self.get_game_page()
        active = text.find(GameState.logged_locator) != -1 or self.codes_blocked(text)
        if active:
            if timeouts.process_check_interval != timeouts.active_game_interval:
                timeouts.process_check_interval = timeouts.active_game_interval
        return active

    def game_inactive(self, text=None):
        if text is None:
            text = self.get_game_page()
        inactive = (self.is_finished(text) or
                    self.not_started(text) or
                    self.about_to_start() or
                    self.not_payed(text) or
                    self.not_approved(text) or
                    self.closed(text) or
                    self.banned_as_bot(text))
        if inactive:
            if timeouts.process_check_interval != timeouts.inactive_game_interval:
                timeouts.process_check_interval = timeouts.inactive_game_interval
        return inactive

    def info_message(self, text=None):
        if text is None:
            text = self.get_game_page()
        return text.find(GameState.info_message_start) != -1

    def not_payed(self, text=None):
        if text is None:
            text = self.get_game_page()
        if self.info_message(text):
            start = text.find(GameState.info_message_start)
            end = text[start:].find(GameState.info_message_end)
            return text[start:start + end].find(GameState.not_payed) != -1
        else:
            return False

    def not_approved(self, text=None):
        if text is None:
            text = self.get_game_page()
        if self.info_message(text):
            start = text.find(GameState.info_message_start)
            end = text[start:].find(GameState.info_message_end)
            return text[start:start + end].find(GameState.not_approved) != -1
        else:
            return False

    def not_started(self, text=None):
        if text is None:
            text = self.get_game_page()
        if self.info_message(text):
            start = text.find(GameState.info_message_start)
            end = text[start:].find(GameState.info_message_end)
            return text[start:start + end].find(GameState.game_start_at) != -1
        else:
            return False

    def about_to_start(self, text=None):
        if text is None:
            text = self.get_game_page()
        if self.info_message(text):
            start = text.find(GameState.info_message_start)
            end = text[start:].find(GameState.info_message_end)
            return text[start:start + end].find(GameState.game_about_to_start) != -1
        else:
            return False

    def closed(self, text=None):
        if text is None:
            text = self.get_game_page()
        if self.info_message(text):
            start = text.find(GameState.info_message_start)
            end = text[start:].find(GameState.info_message_end)
            return text[start:start + end].find(GameState.game_closed) != -1
        else:
            return False

    def banned_as_bot(self, text=None):
        if text is None:
            text = self.get_game_page()
        if text.find(GameState.banned_as_bot_start) != -1:
            start = text.find(GameState.banned_as_bot_start)
            end = text[start:].find(GameState.info_message_end)
            return text[start:start + end].find(GameState.banned_as_bot) != -1
        else:
            return False

    def is_finished(self, text=None):
        if text is None:
            text = self.get_game_page()
        if self.get_finish_message(text) is not None:
            return True
        else:
            return False

    def codes_blocked(self, text=None):
        if text is None:
            text = self.get_game_page()
        return text.find(GameState.blocked_locator) != -1

    def get_game_page(self):
        try:
            # # Use to emulate game page
            # f = codecs.open("mock.htm", encoding='utf-8')
            # game_page = f.read()
            # return game_page
            return self.session.get(
                game_settings.quest_url.format(
                    host=game_settings.game_host,
                    path=game_settings.quest_game_url.format(game_id=game_settings.game_id))).text
        except ConnectionError:
            return ""

    def post_game_page(self, body):
        try:
            # # Use to emulate game page
            # f = codecs.open("mock.htm", encoding='utf-8')
            # game_page = f.read()
            # return game_page
            return self.session.post(
                game_settings.quest_url.format(
                    host=game_settings.game_host,
                    path=game_settings.quest_game_url.format(game_id=game_settings.game_id)),
                params=body).text
        except ConnectionError:
            return ""

    # TODO: to parsers
    def get_level_params(self, text=None):
        if text is None:
            text = self.get_game_page()
        level_id_start = \
            text[text.find(InGame.level_id_locator) +
                 len(InGame.level_id_locator):]
        level_number_start = \
            text[text.find(InGame.level_number_locator) +
                 len(InGame.level_number_locator):]
        level_id = level_id_start[:level_id_start.index(InGame.level_params_end_locator)]
        level_number = level_number_start[:level_number_start.index(InGame.level_params_end_locator)]
        return {"LevelId": int(level_id),
                "LevelNumber": int(level_number)}

    def set_level_params(self, text=None):
        if text is None:
            text = self.get_game_page()
        level_params = self.get_level_params(text)
        self.level_id = level_params["LevelId"]
        self.level_number = level_params["LevelNumber"]
        return level_params

    def try_code(self, code="", username=None):
        if self.handbrake or self.auto_handbrake:
            return GameMessages.HANDBRAKE
        body = {"rnd": self.rnd,
                "LevelId": self.level_id,
                "LevelNumber": self.level_number,
                "LevelAction.Answer": code}
        r = self.post_game_page(body=body)
        result = ''
        if self.not_payed(r):
            return GameMessages.GAME_NOT_PAYED
        if self.not_approved(r):
            return GameMessages.GAME_NOT_APPROVED
        if self.not_started(r):
            return GameMessages.GAME_NOT_STARTED
        elif self.is_finished(r):
            return GameMessages.GAME_FINISHED
        elif self.codes_blocked(r):
            return GameMessages.CODES_BLOCKED
        elif self.closed(r):
            return GameMessages.GAME_FINISHED
        elif self.banned_as_bot(r):
            return GameMessages.BANNED
        if self.level_number != self.get_level_params(r)["LevelNumber"]:
            if r.find(InGame.incorrect_code_locator) == -1 and \
                    r.find(InGame.correct_code_locator) != -1:
                # Collect code if was not entered already
                codes_log.log_code('? ' + code, self.level_number, username)
            return
        if r.find(InGame.incorrect_code_locator) == -1 and \
                r.find(InGame.correct_code_locator) != -1:
            # Save entered codes
            username_found = codes_log.log_code(code, self.level_number, username)
            if username_found is None:
                result = u'\r\n{smile}: {code}'.format(smile=Smiles.CORRECT_CODE,
                                                       code=code)
            else:
                result = u'\r\n{smile}: {code} {dublicate}'.format(
                    smile=Smiles.DUPLICATE_CODE,
                    code=code,
                    dublicate=CommandMessages.DUPLICATE_CODE.format(username=username_found))
        elif r.find(InGame.incorrect_code_locator) != -1:
            result = u'\r\n{smile}: {code}'.format(
                code=code,
                smile=Smiles.WRONG_CODE)
        return result

    def get_all_hints(self, text=None):

        # TODO: To parsers
        # TODO: Add hints with penalties!
        # <h3 class="inline">Штрафная подсказка
        # <div class="spacer"></div>
        # <h3 class="inline">Штрафная подсказка 1</h3>
        # <p>абриколь</p>
        if text is None:
            text = self.get_game_page()
        hints = {}
        hint_text_end = 0
        hint_start = text.find(InGame.hint_number_start_locator)
        while hint_start != -1:
            hint_start += len(InGame.hint_number_start_locator) + hint_text_end
            hint_text_end = hint_start
            hint_end = hint_start + text[hint_start:].find(InGame.hint_number_end_locator)
            hint_number = text[hint_start: hint_end]
            if hint_number.isdigit():
                hint_text_start = \
                    hint_end + \
                    text[hint_end:].find(InGame.hint_text_start_locator) + \
                    len(InGame.hint_text_start_locator)
                hint_text_end = hint_text_start + text[hint_text_start:].find(InGame.hint_text_end_locator)
                hint_text = text[hint_text_start: hint_text_end]
                hint_text = html2text.html2text(hint_text)
                hints.setdefault(int(hint_number), hint_text)
            hint_start = text[hint_text_end:].find(InGame.hint_number_start_locator)
        return hints

    # TODO: To parsers
    def get_task(self, text=None):
        if text is None:
            text = self.get_game_page()
        task_header_start = text.find(InGame.task_header_locator)
        if task_header_start == -1 and text.find(InGame.another_task_header_locator) == -1:
            return
        task_header_start += len(InGame.task_header_locator)
        task_text_start = \
            task_header_start + \
            text[task_header_start:].find(InGame.task_start_locator) + \
            len(InGame.task_start_locator)
        task_text_end = \
            task_text_start + \
            text[task_text_start:].find(InGame.task_end_locator)
        # task_text = self.replace_image_texts(text[task_text_start: task_text_end])
        task_text = text[task_text_start: task_text_end]
        task_text = self.replace_audio_links(task_text)
        task_text = self.replace_iframe_links(task_text)
        return html2text.html2text(task_text)

    def replace_audio_links(self, text):
        """

        :param text:
        :type text: str
        :return:
        """
        while text.find(InGame.audio_start_locator) != -1:
            audio_start = text.find(InGame.audio_start_locator)
            audio_end = audio_start + text[audio_start:].find(InGame.audio_end_locator) + len(InGame.audio_end_locator)
            audio_text = text[audio_start: audio_end]
            link = self.get_source(audio_text)
            text = text.replace(audio_text, link)
        return text

    def replace_iframe_links(self, text):
        """

        :param text:
        :type text: str
        :return:
        """
        while text.find(InGame.iframe_start_locator) != -1:
            iframe_start = text.find(InGame.iframe_start_locator)
            iframe_end = iframe_start + text[iframe_start:].find(InGame.iframe_end_locator) + len(InGame.iframe_end_locator)
            iframe_text = text[iframe_start: iframe_end]
            link = self.get_source(iframe_text)
            text = text.replace(iframe_text, link)
        return text

    @staticmethod
    def get_source(text):
        source_start = text.find(InGame.source_start_locator)
        if source_start != -1:
            source_start += len(InGame.source_start_locator)
            source_end = source_start + text[source_start:].find(InGame.source_end_locator)
            return text[source_start: source_end]

    def get_time_to_ap(self, text=None):
        if text is None:
            text = self.get_game_page()
        ap_start = text.find(InGame.ap_locator)
        if ap_start != -1:
            ap_start += len(InGame.ap_locator)
            ap_end = ap_start + text[ap_start:].find(InGame.ap_end_locator)
            return html2text.html2text(text[ap_start: ap_end])

    def get_time_to_hints(self, text=None):
        time_to_hints = []
        ap_start = text.find(InGame.hint_locator)
        while ap_start != -1:
            ap_end = ap_start + text[ap_start:].find(InGame.hint_end_locator)
            time_to_hints.append(html2text.html2text(text[ap_start: ap_end]))
            text = text.replace(text[ap_start: ap_end], '')
            ap_start = text.find(InGame.hint_locator)
        return time_to_hints

    def get_codes_left_text(self, text=None):
        if text is None:
            text = self.get_game_page()
        codes_left_start = text.find(InGame.codes_left_locator)
        if codes_left_start != -1:
            codes_left_start += len(InGame.codes_left_locator)
            codes_left_end = codes_left_start + text[codes_left_start:].find(InGame.codes_left_end_locator)
            return int(html2text.html2text(text[codes_left_start: codes_left_end]))

    def get_not_payed_message(self, text=None):
        if text is None:
            text = self.get_game_page()
        return GameState.not_payed

    def get_not_approved_message(self, text=None):
        if text is None:
            text = self.get_game_page()
        return GameState.not_approved

    def get_not_started_message(self, text=None):
        if text is None:
            text = self.get_game_page()
        if text.find(GameState.message_start_locator) != -1:
            message_start = text.find(GameState.message_start_locator)
            message_end = text[message_start:].find(GameState.message_end_locator)
            return text[message_start:message_start + message_end]

    def get_about_to_start_message(self, text=None):
        if text is None:
            text = self.get_game_page()
        return GameState.game_about_to_start_text

    def get_closed_message(self, text=None):
        if text is None:
            text = self.get_game_page()
        return GameState.game_closed_text

    def get_banned_as_bot_message(self, text=None):
        if text is None:
            text = self.get_game_page()
        return GameState.game_banned_as_bot_text

    def get_finish_message(self, text=None):
        if text is None:
            text = self.get_game_page()
        finish_start = text.find(GameState.finish_start_locator)
        if finish_start != -1:
            finish_start += len(GameState.finish_start_locator)
            finish_end = finish_start + text[finish_start:].find(GameState.finish_end_locator)
            return html2text.html2text(text[finish_start: finish_end])

    def answer_limit(self, text=None):
        if text is None:
            text = self.get_game_page()
        answer_text_start = text.find(InGame.answer_text_start_locator)
        if answer_text_start != -1:
            answer_text_start += len(InGame.answer_text_start_locator)
            answer_text_end = answer_text_start + text[answer_text_start:].find(InGame.answer_text_end_locator)
            answer_text = text[answer_text_start: answer_text_end]
            limit_start = answer_text.find(InGame.limit_start_locator)
            if limit_start != -1:
                limit_end = limit_start + answer_text[limit_start:].find(InGame.limit_end_locator)
                return html2text.html2text(answer_text[limit_start:limit_end])

    def get_org_message(self, text=None):
        if text is None:
            text = self.get_game_page()
        org_message_start = text.find(InGame.org_message_locator)
        if org_message_start != -1:
            org_message_start += len(InGame.org_message_locator)
            org_message_end = org_message_start + text[org_message_start:].find(InGame.org_message_end_locator)
            org_message = html2text.html2text(text[org_message_start: org_message_end])
            org_message = org_message.replace('[', '', 1).replace(']', '', 1)
            delete_start = org_message.index('(')
            delete_end = org_message.index(')') + 1
            org_message = org_message[:delete_start] + org_message[delete_end:]
            return html2text.html2text(org_message)

    def get_codes_gap(self, text=None):
        if text is None:
            text = self.get_game_page()
        start = 0
        codes = []
        code_index = text.find(InGame.not_entered_code_locator[start:])
        # Find all not entered codes
        while code_index != -1:
            text_reversed = text[code_index::-1]
            code_name_start = text_reversed.find(InGame.code_name_locator_start) + len(InGame.code_name_locator_start)
            code_name_end = text_reversed.find(InGame.code_name_locator_end)
            code_name = text_reversed[code_name_start:code_name_end][::-1]
            codes.append(code_name)
            start = code_index + len(InGame.not_entered_code_locator)
            code_index = text[start:].find(InGame.not_entered_code_locator)
            if code_index != -1:
                code_index += start
        # Test example of codes
        # codes = ['1', '2', '3', '5', '6', '8', '9', '10',
        #          '11', '12', '13', '14', '15', '16', '17',
        #          '18', '19', '20', '21', '22', '23', '24',
        #          '25', '26', '27', '28', '29', '30', '31',
        #          '32', '33', '34', '35', '36', '37', '38',
        #          '39', '40', '51', '52', '53', '54', '64',
        #          '67', '68', '77', '101', '111', '112',
        #          '113', '114', '177']

        # Group codes
        numbers = []
        not_numbers = []
        for code in codes:
            if code.isdigit():
                numbers.append(code)
            else:
                not_numbers.append(code)
        codes_grouped = ''
        if len(numbers):
            consistent_codes = []
            separated_by_intervals = []
            if len(numbers):
                consistent_codes.append(int(numbers[0]))
                # TODO:
                # Crutch in order not to lose last code number
                # If you don't like it - feel free to create new algorithm!
                numbers.append(0)
            for code in numbers[1:]:

                if int(code) - 1 == consistent_codes[-1]:
                    consistent_codes.append(int(code))
                else:
                    if len(consistent_codes) == 2:
                        separated_by_intervals.append([consistent_codes[0], consistent_codes[0]])
                        separated_by_intervals.append([consistent_codes[1], consistent_codes[1]])
                    else:
                        separated_by_intervals.append([consistent_codes[0], consistent_codes[-1]])
                    consistent_codes = [int(code)]

            decade = None
            for code_pair in separated_by_intervals:
                # Format by decades
                current_decade = divmod(int(code_pair[0]), 10)[0]
                if decade is None:
                    decade = current_decade
                if current_decade != decade:
                    codes_grouped = codes_grouped[:-2]
                    codes_grouped += '\r\n'
                    decade = current_decade
                if code_pair[0] == code_pair[1]:
                    codes_grouped += str(code_pair[0]) + ', '
                else:
                    # Add intervals
                    codes_grouped += str(code_pair[0]) + ' — ' + str(code_pair[1]) + ', '
            codes_grouped = codes_grouped[:-2]
            codes_grouped += '\r\n'
        if len(not_numbers):
            for code in not_numbers:
                codes_grouped += code + '\r\n'
        return codes_grouped
