# -*- coding: utf-8 -*-


class GameState(object):
    info_message_start = u'<div class="infomessage" style="display:block">'
    info_message_end = u'</div>'
    game_start_at = u'Игра начнется в'
    game_about_to_start = u'Игра начнется через'
    game_about_to_start_text = u'Скоро начнётся игра!'
    game_closed = u'Игра уже закончилась'
    game_closed_text = u'Игра уже закончилась'

    not_payed = u"""Ваша команда не сделала взнос на эту игру"""

    finished = u'<font size="+2"><span id="animate">Поздравляем!!!</span></font>'

    message_start_locator = u'Игра начнется в'
    message_end_locator = u'<span'

    finish_start_locator = u'<div class="t_center">'
    finish_end_locator = u'</div>'

    logged_locator = u'<label for="Answer">'
    blocked_locator = u'<div class="blocked"><div>вы сможете ввести код через'

    banned_as_bot_start = u'<div id="Splash">'
    banned_as_bot = u'Ваши запросы классифицированы как запросы робота.'
    game_banned_as_bot_text = u'Ваши запросы классифицированы как запросы робота. ' \
                              u'Попробуйте залогиниться в систему и запустите бота заново.'


class InGame(object):
    level_id_locator = u'<input type="hidden" name="LevelId" value="'
    level_number_locator = u'<input type="hidden" name="LevelNumber" value="'
    level_params_end_locator = '"'

    incorrect_code_locator = u'<span class="color_incorrect" id="incorrect">'
    correct_code_locator = u'<span class="color_correct">'

    hint_number_start_locator = u'<h3>Подсказка '
    hint_number_end_locator = u'</h3>'
    hint_text_start_locator = u'<p>'
    hint_text_end_locator = u'</p>'

    task_header_locator = u'<h3>Задание</h3>'
    another_task_header_locator = u'<h2>Уровень <span>'
    task_start_locator = u'<p>'
    task_end_locator = u'</p>'

    audio_start_locator = u'<audio'
    audio_end_locator = u'/audio>'

    iframe_start_locator = u'<iframe'
    iframe_end_locator = u'</iframe>'

    source_start_locator = u'src="'
    source_end_locator = u'"'

    ap_locator = u'<h3 class="timer">'
    ap_end_locator = u'</h3>'

    hint_locator = u'<span class="color_dis"><b>Подсказка'
    hint_end_locator = u'</span>'

    codes_left_locator = u'осталось закрыть'
    codes_left_end_locator = u')</span>'

    answer_text_start_locator = u'<form method="post">'
    answer_text_end_locator = u'</form>'
    limit_start_locator = u'Не более'
    limit_end_locator = u'</label>'

    org_message_locator = u"""<p class="globalmess">"""
    org_message_end_locator = u"""</p>"""

    not_entered_code_locator = u"""<span class="color_dis">код не введён</span>"""
    code_name_locator_end = u">p<"
    code_name_locator_start = u"< :"
