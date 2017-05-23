# -*- coding: utf-8 -*-
from config import config


class Smiles:
    TASK = unichr(55356) + unichr(57152)
    HINTS = unichr(55356) + unichr(57119)
    CORRECT_CODE = unichr(9989)
    WRONG_CODE = unichr(10060)
    LIMIT = unichr(55357) + unichr(56489)
    ORG_MESSAGE = unichr(55357) + unichr(56596)
    ALERT = unichr(9757) + unichr(65039)
    CODES_LEFT = unichr(9757) + unichr(65039)
    CODE_LEFT = unichr(10071) + unichr(65039)
    ONE_CODE_LEFT = unichr(8252) + unichr(65039)
    AP = unichr(9201)
    TASK_EDITED = unichr(8265) + unichr(65039)


class CommonMessages:
    PAUSED = u'Я на паузе.'
    ALREADY_PAUSED = u'Не поверишь. Я и так на паузе'
    ALREADY_WORKING = u'Я тебя сейчас наверное удивлю, но я и так работаю.'
    BYE = [u"Всё, давай, пока!",
           u"Давай, до свидания!",
           u"До скорых встреч, уважаемый."]
    AFFIRMATIVE = [u"Я понял тебя, братан",
                   u"Замётано",
                   u"Так точно"]
    UNKNOWN = u"Я тебя не понимаю"
    NOT_GROUP_CHAT = u"Напиши мне в командном чате, а не в личку."
    DO_PAUSE = u"Так. Не трогаю пока ничего тут"
    DO_RESUME = u"И снова здравствуйте!"
    LETS_GO = u"Воо-оо-оойтии-ии-и в игруу-уу-уу"
    DISAPPROVE = u"Если ты им не доверяешь - значит и я."
    CONNECTION_OK_MESSAGES = u"---*Авторизация на сайте успешна!*---"
    PLEASE_APPROVE_MESSAGES = u"---*Для дальнейшей работы выполни команду* /approve *в игровом чате*---"
    ACCESS_VIOLATION_MESSAGES = u"*Данная операция запрещена для вас, уважаемый.*"
    NO_GROUP_CHAT_MESSAGES = u"Я не доверяю этой группе людей."
    NOT_FOR_GROUP_CHAT_MESSAGES = [u"Такое лучше писать в личку."]


class BotSystemMessages:
    NEW_TOKEN = u"""Текущий токен: *{token}*\r\n Введи новый токен или *NO* для отмены операции"""
    TOKEN_CHANGED = u"""Токен был изменен"""
    CODE_LIMIT = u"""Введи новое ограничение на перебор кодов или *NO* для отмены операции"""
    CODE_LIMIT_CHANGED = u"""Ограничение на перебор кодов было изменено"""
    TOKEN_CANCELLED = u"""Изменение токена отменено"""
    OPERATION_CANCELLED = u"""Операция отменена"""
    CODE_LIMIT_CANCELLED = u"""Ограничение на перебор кодов не было изменено"""
    CONFIRM_DELETEION = u"""Эту операцию нельзя отменить. Для подтверждения напиши *"YES"* """
    ADMIN_CLEARED = u"""Все админы были удалены."""
    FIELD_CLEARED = u"""Все полевые игроки были удалены."""
    KC_CLEARED = u"""Все штабные игроки были удалены."""
    ERRORS_CLEARED = u"""Лог ошибок очищен."""
    UNKNOWN_CLEARED = u"""Лог неопознанных пользователей очищен."""
    MEMORY_CLEARED = u"""Лог заданий и введённых кодов удалён."""
    BOT_WAS_RESET = u"Состояние бота было сброшено на начальное."


class CommandMessages:
    NO_CODE_FOUND = u'_Нет кодов для вбития. Попробуй ещё раз. Формат: /c long code или /cc code 1 code2_'
    DUPLICATE_CODE = u'\r\n{code}: уже вбил *{username}*'
    CODE_LIMIT = u"""Перебор такого количества кодов запрещён! Текущий лимит: {codelimit}"""
    NO_USER_ID = u"""Нет user id для добавления. Пример:
/addadmin 123456"""
    NO_MESSAGE = u"""Нет user id для сообщения. Пример:
/command 123456"""
    NO_TASK_ID = u"""Нет id уровня. Пример:
/codes 123456"""
    WRONG_LEVEL_ID = u"""Нет сохраненного уровня с указанным id"""
    FIELD_TRIED_CODE = u"""<b>{nickname}</b>:
{codes}"""


class SettingsMessages:
    ENTER_NEW_PASS = u"""Текущий инвайт-код: {code}.
Введите новый:"""
    PASS_WAS_CHANGED = u"""Пароль был изменён с *{code1}* на *{code2}*"""
    DUPLICATE_PASS = u"""Данный пароль уже используется, придумай другой."""

    GIVE_ME_LOGIN = u"Давай мне свой *логин* для игры."
    GIVE_ME_PASSWORD = u"Давай мне свой *пароль*."
    GIVE_ME_HOST = u"На каком *домене* игра?"
    GIVE_ME_GAME = u"Какой *номер игры*?"
    GIVE_ME_NEW_LOGIN = u"Текущий логин: *{login}*\r\nВведи новый:"
    GIVE_ME_NEW_PASSWORD = u"Текущий пароль: *{password}*\r\nВведи новый:"
    GIVE_ME_NEW_HOST = u"Текущий хост игры: *{host}*\r\nВведи новый:"
    GIVE_ME_NEW_GAME = u"Текущий номер игры: *{game}*\r\nВведи новый:"
    TAG_FIELD = u"""Отмечать ли полевых игроков при получении нового задания?
*YES* - да, *NO* - нет, *CANCEL* - отменить"""
    SETTINGS_WERE_CHANGED = u"---*Настройки бота были изменены!*---"
    SETTINGS_WERE_SAVED = u"Настройки были сохранены"
    SETTINGS_WERE_NOT_SAVED = u"Проблема при записи настроек. Проверьте права доступа."
    SETTINGS_WERE_NOT_CHANGED = u"Настройки не были изменены."
    CONNECTION_PROBLEM = u"---*Проблемы с авторизацией на сайте!*---"
    CHECK_SETTINGS = u"---*Проверьте настройки!*---"
    NEED_SAVE = u"""
Для сохранения измений после перезапуска - сохрани настройки в базу.""" \
        if not config.autosave else ''


class UserMessages:
    HELLO_NEW_USER = u"""Добро пожаловать в ряды нашей доблестной команды.
Для начала рекомендую начать с просмотра доступных команд: /help
*ВНИМАНИЕ!*
Все следующие сообщения, которые ты будешь писать мне в личку - будут автоматически вбиваться в систему.
Будь внимателен!"""
    HELLO_NEW_ADMIN = u"""Добро пожаловать в ряды нашей доблестной команды.
Для начала рекомендую начать с просмотра доступных команд: /help"""

    NEW_ADMIN_WAS_ADDED = u"""Новый админ добавлен: {user_id} : {nickname}.""" + SettingsMessages.NEED_SAVE
    NEW_FIELD_WAS_ADDED = u"""Новый полевой игрок добавлен: {user_id} : {nickname}.""" + SettingsMessages.NEED_SAVE
    NEW_KC_WAS_ADDED = u"""Новый штабной игрок добавлен: {user_id} : {nickname}.""" + SettingsMessages.NEED_SAVE
    DUPLICATE_USER_ID = u"""Такой пользователь уже есть в базе. Добавление прервано."""
    CANNOT_DELETE_ADMIN = u"""Нельзя удалить последнего админа."""
    WRONG_USER_ID = u"""Неверный id пользователя"""
    DELETE_USER_ID = u"""Текущие пользователи:
{current_ids}
Введите id, который нужно удалить."""
    USER_DELETED = u"""Пользователь удалён.""" + SettingsMessages.NEED_SAVE


class GameMessages:
    GAME_NOT_PAYED = u"\r\nВаша команда не сделала взнос на игру."
    GAME_NOT_STARTED = u"\r\nИгра ещё не началась."
    GAME_FINISHED = u"\r\nИгра окончена."
    CODES_BLOCKED = u"\r\nВвод кодов заблокирован."

    TASK_MESSAGE = u"""
<b>---------------------------</b>
<b>Задание {level_number}</b>
<b>---------------------------</b>

{task}"""

    NEW_TASK = u"""
{smile}<b>Новый уровень!</b>
{task}""".format(smile=Smiles.TASK, task=TASK_MESSAGE)
    NEW_HINT = u"""
{smile}<b>Новая подсказка!</b>
<b>---------------------------</b>
<b>Подсказка {hint_number}</b>
<b>---------------------------</b>

{hint}"""
    NO_HINTS = u"""Подсказки ещё не приходили"""
    TASK_EDITED = Smiles.TASK_EDITED + u"""
<b>Задание было изменено!</b>
<b>---------------------------</b>

{task}"""

    CODES_LEFT_TEXT = {1: Smiles.ONE_CODE_LEFT + u'<b>Остался {codes} код!</b>',
                       2: Smiles.CODE_LEFT + u'Осталось {codes} кода!',
                       3: Smiles.CODE_LEFT + u'Осталось {codes} кода!',
                       4: Smiles.CODE_LEFT + u'Осталось {codes} кода!',
                       'all': Smiles.CODES_LEFT + u'Всего кодов осталось: {codes}'}


class FileMessages:
    NO_DATA_TO_DISPLAY = u"Нет данных для отображения."


class HelpMessages:
    STATUS = u"""
Статус дружочка: {paused}
Активная группа: {chat_id}
Соединение к игровому серверу: {game_connection}
Текущий номер задания: {game_level_id}
Показанные подсказки: {game_hint_id}"""

    INFO = u"""
Логин: {login}
Пароль: {password}
Хост: {host}
Игра: {game_id}
Активная группа: {chat_id}
Токен: {token}
rnd: {rnd}
Лимит на вбитие кодов: {codelimit}
Отмечать поле при новом задании: {tag_field}
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

    PAUSED = {False: u"Активный",
              True: u"На паузе"}

    GAME_CONNECTION = {True: u"Активно",
                       False: u"Ошибка"}

    REGULAR_HELP = u"""
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

    ADMIN_HELP = u"""
*Админ-секция:*
{approve} : Добавить чат в список доверенных
{disapprove} : Удалить чат из списка доверенных

{info} : Вывести детальную информацию о боте
{edit} : Изменить текущие настройки бота
{save} : Перезаписать настройки бота по-умолчанию
{reset} : Обнулить список полученных заданий/подсказок
{token}: Изменить токен бота
{codes_limit}: Изменить максимальное количество кодов для вбития одной пачкой
{login}: Изменить логин в игре
{password}: Изменить пароль в игре
{host}: Изменить хост игры (без http://)
{game}: Изменить номер игры

{pause} : Прекратить отслеживание заданий и вбитие кодов
{resume} : Возобновить отслеживание заданий и вбитие кодов
{stop} : Закончить работу с ботом

{addadmin}: Добавить нового админа. Необходимо указать id пользователя
{addfield}: Добавить нового полевого игрока. Необходимо указать id пользователя
{addkc}: Добавить нового штабного игрока. Необходимо указать id пользователя
{deleteadmin}: Удалить админа по его id
{deletefield}: Удалить полевого игрока по его id
{deletekc}: Удалить штабного игрока по его id
{cleanadmin}: Очистить список админов
{cleanfield}: Очистить список полевых игроков
{cleankc}: Очистить список штабных игроков

{eap}: Изменить инвайт-код для админов
{efp}: Изменить инвайт-код для полевых игроков
{ekp}: Изменить инвайт код для штабных игроков

{alert}: Вывести объявление в групповой чат с тегом всего поля
{chat_message}: Вывести объявление в групповой чат
{message}: Написать от имени бота указанному id
{message_admin}: Сделать рассылку в личку всем админам
{message_field}: Сделать рассылку в личку всему полю
{message_kc}: Сделать рассылку в личку всему КЦ
{tag_field}: Редактировать оповещение игроков при получении нового задания

{source}: Отправить текущую страницу
{errors}: Отправить лог ошибок
{clean_errors}: Очистить лог ошибок
{unknown}: Отправить лог запросов от неизвестных пользователей
{clean_unknown}: Очистить лог запросов от неизвестных
{clean_memory}: Очистить лог заданий и введённых кодов

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
        cleanadmin=config.cleanadmin_command,
        cleanfield=config.cleanfield_command,
        cleankc=config.cleankc_command,
        eap=config.edit_admin_pass,
        efp=config.edit_field_pass,
        ekp=config.edit_kc_pass,
        message=config.message_command,
        alert=config.alert_command,
        chat_message=config.chat_message_command,
        message_admin=config.message_admin_command,
        message_field=config.message_field_command,
        message_kc=config.message_kc_command,
        source=config.send_source_command,
        errors=config.send_errors_command,
        unknown=config.send_unknown_command,
        codes_limit=config.codes_limit_command,
        login=config.login_command,
        game=config.game_command,
        password=config.pass_command,
        host=config.host_command,
        clean_errors=config.cleanerrors_command,
        clean_unknown=config.cleanunknown_command,
        tag_field=config.tag_field_command,
        clean_memory=config.clean_memory_command,
        regular=REGULAR_HELP)
