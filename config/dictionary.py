# -*- coding: utf-8 -*-
from config import config

TASK_APPEND = unichr(55356) + unichr(57152)
HINTS_APPEND = unichr(55356) + unichr(57119)
CORRECT_CODE_APPEND = unichr(9989)
WRONG_CODE_APPEND = unichr(10060)
LIMIT_APPEND = unichr(55357) + unichr(56489)
ORG_MESSAGE_APPEND = unichr(55357) + unichr(56596)
CODES_LEFT_MESSAGE_APPEND = unichr(9757) + unichr(65039)
CODE_LEFT_MESSAGE_APPEND = unichr(10071) + unichr(65039)
ONLY_CODE_LEFT_MESSAGE_APPEND = unichr(8252) + unichr(65039)
AP_MESSAGE_APPEND = unichr(9201)
TASK_EDITED_MESSAGE_APPEND = unichr(8265) + unichr(65039)

PAUSED_MESSAGE = u'Я на паузе.'
ALREADY_PAUSED_MESSAGE = u'Не поверишь. Я и так на паузе'
RESUME_MESSAGE = u'Я тебя сейчас наверное удивлю, но я и так работаю.'
BYE_MESSAGES = [u"Всё, давай, пока!",
                u"Давай, до свидания!",
                u"До скорых встреч, уважаемый."]
AFFIRMATIVE_MESSAGES = [u"Я понял тебя, братан",
                        u"Замётано",
                        u"Так точно"]
UNKNOWN_MESSAGES = [u"Я тебя не понимаю"]
NOT_GROUP_CHAT_MESSAGES = [u"Напиши мне в командном чате, а не в личку."]
START_PAUSE_MESSAGES = [u"Так. Не трогаю пока ничего тут"]
END_PAUSE_MESSAGES = [u"И снова здравствуйте!"]
LETS_GO_MESSAGES = [u"Воо-оо-оойтии-ии-и в игруу-уу-уу"]
DISAPPROVE_MESSAGES = [u"Если ты им не доверяешь - значит и я."]
NO_CODE_FOUND_MESSAGE = u'_Нет кодов для вбития. Попробуй ещё раз. Формат: /c long code или /cc code 1 code2_'

NEW_TOKEN_MESSAGE = u"""Введи новый токен бота или *NO* для отмены операции"""
CODE_LIMIT_MESSAGE = u"""Введи новое ограничение на перебор кодов или *NO* для отмены операции"""
TOKEN_CHANGED = u"""Токен был изменен"""
CODE_LIMIT_CHANGED = u"""Ограничение на перебор кодов было изменено"""
TOKEN_CANCELLED = u"""Изменение токена отменено"""
CODE_LIMIT_CANCELLED = u"""Ограничение на перебор кодов не было изменено"""
CODE_LIMIT = u"""Перебор такого количества кодов запрещён! Текущий лимит: {codelimit}"""
CONFIM_DELETEION = u"""Эту операцию нельзя отменить. Для подтверждения напиши *"YES"* """
ADMIN_CLEARED = u"""Все админы были удалены."""
FIELD_CLEARED = u"""Все полевые игроки были удалены."""
KC_CLEARED = u"""Все штабные игроки были удалены."""
HELLO_NEW_USER = u"""Добро пожаловать в ряды нашей доблестной команды.
Для начала рекомендую начать с просмотра доступных команд: /help
*ВНИМАНИЕ!*
Все следующие сообщения, которые ты будешь писать мне в личку - будут автоматически вбиваться в систему.
Будь внимателен!"""
HELLO_NEW_ADMIN = u"""Добро пожаловать в ряды нашей доблестной команды.
Для начала рекомендую начать с просмотра доступных команд: /help"""
NO_USER_ID_MESSAGE = u"""Нет user id для добавления. Пример:
/addadmin 123456"""
NO_MESSAGE = u"""Нет user id для сообщения. Пример:
/command 123456"""
NO_TASK_ID = u"""Нет id уровня. Пример:
/codes 123456"""
NEED_SAVE = u"""
Для сохранения измений после перезапуска - сохраните настройки в базу.""" \
    if not config.autosave else ''
NEW_ADMIN_WAS_ADDED = u"""Новый админ добавлен: {user_id} : {nickname}.""" + NEED_SAVE
NEW_FIELD_WAS_ADDED = u"""Новый полевой игрок добавлен: {user_id} : {nickname}.""" + NEED_SAVE
NEW_KC_WAS_ADDED = u"""Новый штабной игрок добавлен: {user_id} : {nickname}.""" + NEED_SAVE
DUPLICATE_USER_ID = u"""Такой пользователь уже есть в базе. Добавление прервано."""
CANNOT_DELETE_ADMIN_MESSAGE = u"""Нельзя удалить последнего админа."""
WRONG_USER_ID_MESSAGE = u"""Неверный id пользователя"""
WRONG_LEVEL_ID_MESSAGE = u"""Нет сохраненного уровня с указанным id"""
DELETE_USER_ID_MESSAGE = u"""Текущие пользователи:
{current_ids}
Введите id, который нужно удалить."""
USER_DELETED_MESSAGE = u"""Пользователь удалён.""" + NEED_SAVE

FIELD_TRIED_CODE = u"""{nickname}:
{codes}"""

ENTER_NEW_PASS = u"""Текущий инвайт-код: {code}.
Введите новый:"""
PASS_WAS_CHANGED = u"""Пароль был изменён с {code1} на {code2}"""
DUPLICATE_PASS = u"""Данный пароль уже используется, придумайте другой."""

GIVE_ME_LOGIN = [u"Давай мне свой *логин* для игры."]
GIVE_ME_PASSWORD = [u"Давай мне свой *пароль*."]
GIVE_ME_HOST = [u"На каком *домене* игра?"]
GIVE_ME_GAME = [u"Какой *номер игры*?"]
SETTINGS_WERE_CHANGED_MESSAGES = [u"---*Настройки бота были изменены!*---"]
SETTINGS_WERE_SAVED_MESSAGES = [u"Настройки были сохранены"]
SETTINGS_WERE_NOT_SAVED_MESSAGES = [u"Проблема при записи настроек. Проверьте права доступа."]
CONNECTION_PROBLEM_MESSAGES = [u"---*Проблемы с авторизацией на сайте!*---"]
CHECK_SETTINGS_MESSAGES = [u"---*Проверьте настройки!*---"]
CONNECTION_OK_MESSAGES = [u"---*Авторизация на сайте успешна!*---"]
PLEASE_APPROVE_MESSAGES = [
    u"---*Для дальнейшей работы выполни команду* /approve *в игровом чате*---"]
TOO_MUCH_ATTEMPTS_MESSAGES = [
    u"---*Слишком много неуспешных попыток авторизоваться. *---"]
ACCESS_VIOLATION_MESSAGES = [u"*Данная операция запрещена для вас, уважаемый.*"]
NO_GROUP_CHAT_MESSAGES = [u"Я не доверяю этой группе людей."]
NOT_FOR_GROUP_CHAT_MESSAGES = [u"Такое лучше писать в личку."]

GAME_FINISHED_MESSAGE = u"\r\nИгра окончена."
CODES_BLOCKED_MESSAGE = u"\r\nВвод кодов заблокирован."
NO_DATA_TO_DISPLAY = u"Нет данных для отображения."

STATUS_MESSAGE = u"""
Статус дружочка: {paused}
Активная группа: {chat_id}
Соединение к игровому серверу: {game_connection}
Текущий номер задания: {game_level_id}
Показанные подсказки: {game_hint_id}"""

INFO_MESSAGE = u"""
Логин: {login}
Пароль: {password}
Хост: {host}
Игра: {game_id}
Активная группа: {chat_id}
Токен: {token}
rnd: {rnd}
Лимит на вбитие кодов: {codelimit}
-------------------------------
Инвайт-код для админов: {admin_passphrase}
Инвайт-код для поля: {field_passphrase}
Инвайт-код для КЦ: {kc_passphrase}
Активные админы: {admins}
Полевые игроки: {fields}
Штабные игроки: {kcs}
-------------------------------
Запущен: {time_start}
Ошибок: {bot_errors}
Запросов от неизвестных: {unknown_users}
"""
BOT_WAS_RESET_MESSAGE = u"Состояние бота было сброшено на начальное."

PAUSED_STATUS_MESSAGES = {False: u"Активный",
                          True: u"На паузе"}

GAME_CONNECTION_MESSAGES = {True: u"Активно",
                            False: u"Ошибка"}
TASK_MESSAGE = u"""
<b>---------------------------</b>
<b>Задание {level_number}</b>
<b>---------------------------</b>

{task}"""

NEW_TASK_MESSAGE = u"""
{smile}<b>Новый уровень!</b>
{task}""".format(smile=TASK_APPEND, task=TASK_MESSAGE)
NEW_HINT_MESSAGE = u"""
{smile}<b>Новая подсказка!</b>
<b>---------------------------</b>
<b>Подсказка {hint_number}</b>
<b>---------------------------</b>

{hint}"""
NO_HINTS = u"""Подсказки ещё не приходили"""
TASK_EDITED_MESSAGE = TASK_EDITED_MESSAGE_APPEND + u"""
<b>Задание было изменено!</b>
<b>---------------------------</b>

{task}"""

CODES_LEFT_TEXT = {1: ONLY_CODE_LEFT_MESSAGE_APPEND + u'<b>Остался {codes} код!</b>',
                   2: CODE_LEFT_MESSAGE_APPEND + u'Осталось {codes} кода!',
                   3: CODE_LEFT_MESSAGE_APPEND + u'Осталось {codes} кода!',
                   4: CODE_LEFT_MESSAGE_APPEND + u'Осталось {codes} кода!',
                   'all': CODES_LEFT_MESSAGE_APPEND + u'Всего кодов осталось: {codes}'}

REGULAR_HELP_MESSAGE = u"""
{code}: Вбить один код целиком. Пример: {code} один длинный код
{codes}: Вбить несколько кодов, разделённых пробелом. Пример: {codes} код1 код2 код3
{task}: Повторно вывести задание. Пример: {task} 13
{codes_history}: Вывести введённые коды с указанного задания. Пример: {codes_history} 12
{hints}: Повторно вывести список всех подсказок
{status}: Показать текущий статус бота
{help}: Вывести помощь
""".format(
    code=config.code_command[0],
    codes=config.codes_command[0],
    task=config.task_command,
    hints=config.hints_command,
    status=config.status_command,
    codes_history=config.codes_history_command,
    help=config.help_command)

ADMIN_HELP_MESSAGE = u"""
*Админ-секция:*
{approve} : Добавить чат в список доверенных
{disapprove} : Удалить чат из списка доверенных

{info} : Вывести детальную информацию о боте
{edit} : Изменить текущие настройки бота
{save} : Перезаписать настройки бота по-умолчанию
{reset} : Обнулить список полученных заданий/подсказок
{token}: Изменить токен бота

{pause} : Прекратить отслеживание заданий и вбитие кодов
{resume} : Возобновить отслеживание заданий и вбитие кодов
{stop} : Закончить работу с ботом

{addadmin}: Добавить нового админа. Необходимо указать id пользователя
{addfield}: Добавить нового полевого игрока. Необходимо указать id пользователя
{addkc}: Добавить нового штабного игрока. Необходимо указать id пользователя
{deleteadmin}: Удалить админа по его id
{deletefield}: Удалить полевого игрока по его id
{deletekc}: Удалить штабного игрока по его id
{clearadmin}: Очистить список админов
{clearfield}: Очистить список полевых игроков
{clearkc}: Очистить список штабных игроков

{eap}: Изменить инвайт-код для админов
{efp}: Изменить инвайт-код для полевых игроков
{ekp}: Изменить инвайт код для штабных игроков

{alert}: Вывести объявление в групповой чат с тегом всего поля
{message}: Написать от имени бота указанному id
{message_admin}: Сделать рассылку в личку всем админам
{message_field}: Сделать рассылку в личку всему полю
{message_kc}: Сделать рассылку в личку всему КЦ

{source}: Отправить текущую страницу
{errors}: Отправить лог ошибок
{unknown}: Отправить лог запросов от неизвестных пользователей

*Пользовательские функции:*
{regular}
""".format(
    approve=config.approve_command,
    disapprove=config.disapprove_command,
    token=config.token_command,
    edit=config.edit_command,
    save=config.save_command,
    reset=config.reset_command,
    pause=config.pause_command,
    stop=config.stop_command,
    resume=config.resume_command,
    info=config.info_command,
    help=config.help_command,
    addadmin=config.add_admin_command,
    addfield=config.add_field_command,
    addkc=config.add_kc_command,
    deleteadmin=config.delete_admin_command,
    deletefield=config.delete_field_command,
    deletekc=config.delete_kc_command,
    clearadmin=config.clearadmin_command,
    clearfield=config.clearfield_command,
    clearkc=config.clearkc_command,
    eap=config.edit_admin_pass,
    efp=config.edit_field_pass,
    ekp=config.edit_kc_pass,
    message=config.message_command,
    alert=config.alert_command,
    message_admin=config.message_admin_command,
    message_field=config.message_field_command,
    message_kc=config.message_kc_command,
    source=config.send_source_command,
    errors=config.send_errors_command,
    unknown=config.send_unknown_command,
    regular=REGULAR_HELP_MESSAGE)
