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
                u"До скорых встреч, уважаемый.",
                u"Спасибо, пойду спать."]
AFFIRMATIVE_MESSAGES = [u"Я понял тебя, братан",
                        u"Замётано",
                        u"Так точно"]
UNKNOWN_MESSAGES = [u"Я тебя не понимаю"]
NOT_GROUP_CHAT_MESSAGES = [u"Напиши мне в групповом чате, а не в личку."]
START_PAUSE_MESSAGES = [u"Так. Не трогаю пока ничего тут"]
END_PAUSE_MESSAGES = [u"И снова здравствуйте!"]
LETS_GO_MESSAGES = [u"Воо-оо-оойтии-ии-и в игруу-уу-уу"]
DISAPPROVE_MESSAGES = [u"Если ты им не доверяешь - значит и я."]
NO_CODE_FOUND_MESSAGE = u'_Нет кодов для вбития. Попробуй ещё раз. Формат: /c long code или /cc code 1 code2_'
CREATE_PASSPHRASE_FOR_ADD_ADMIN = u"""
Для добавления нового админа необходимо придумать пароль.
Этот пароль необходимо дать новому админу.
После того, как новый админ напишет этот пароль мне в личку - админ будет добавлен.

Обрати внимание! До тех пор, пока новый админ не напишет мне пароль,
или пока ты не скажешь мне /cancel - бот не будет обрабатывать другие команды!"""
WAITING_FOR_NEW_ADMIN = u"""
Ок, теперь дай этот пароль новому админу, пускай он напишет мне его в личку.
Если ты передумал - напиши мне /cancel"""
WAITING_FOR_NEW_ADMIN_WAS_CANCELED = u"""Добавление нового админа остановлено. Админ не добавлен."""
WAITING_FOR_NEW_ADMIN_WAS_FINISHED = u"""Новый админ добавлен. Его id : {admin_id}.
Для сохранения измений после перезапуска - сохраните настройки в базу."""
DUPLICATE_ADMIN_ID = u"""Такой админ уже есть в базе. Добавление админа прервано."""
CANNOT_DELETE_ADMIN_MESSAGE = u"""Нельзя удалить последнего админа."""
ADMIN_NOT_FOUND_MESSAGE = u"""Неверный id админа"""
DELETE_ADMIN_ID_MESSAGE = u"""Введите id админа, который нужно удалить."""
ADMIN_DELETED_MESSAGE = u"""Админ удалён. Для сохранения измений после перезапуска - сохраните настройки в базу."""

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
Активные админы: {admins}"""
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
TASK_EDITED_MESSAGE = TASK_EDITED_MESSAGE_APPEND + u"""
<b>Задание было изменено!</b>
<b>---------------------------</b>

{task}"""

CODES_LEFT_TEXT = {1: ONLY_CODE_LEFT_MESSAGE_APPEND + u'<b>Остался {codes} код!</b>',
                   2: CODE_LEFT_MESSAGE_APPEND + u'Осталось {codes} кода!',
                   3: CODE_LEFT_MESSAGE_APPEND + u'Осталось {codes} кода!',
                   4: CODE_LEFT_MESSAGE_APPEND + u'Осталось {codes} кода!',
                   'all': CODES_LEFT_MESSAGE_APPEND + u'Всего кодов осталось: {codes}'}

ADMIN_HELP_MESSAGE = u"""
Админ-секция:
{approve} : Добавить чат в список доверенных
{disapprove} : Удалить чат из списка доверенных

{edit} : Изменить текущие настройки бота
{save} : Перезаписать настройки бота по-умолчанию
{reset} : Обнулить список полученных заданий/подсказок

{pause} : Прекратить отслеживание заданий и вбитие кодов
{resume} : Возобновить отслеживание заданий и вбитие кодов
{stop} : Закончить работу с ботом

Пользовательские функции:
{code} : Вбить один код целиком. Пример: {code} один длинный код
{codes} : Вбить несколько кодов, разделённых пробелом. Пример: {codes} код1 код2 код3
{gap} : Вывести список отсутсвующих кодов
{task} : Повторно вывести текущее задание
{hints} : Повторно вывести список всех подсказок

{status} : Показать текущий статус бота
{info} : Вывести детальную информацию о настройках бота
{help} : Вывести помощь
""".format(
    code=config.code_command[0],
    codes=config.codes_command[0],
    gap=config.gap_command,
    task=config.task_command,
    hints=config.hints_command,
    approve=config.approve_command,
    disapprove=config.disapprove_command,
    edit=config.edit_command,
    save=config.save_command,
    reset=config.reset_command,
    pause=config.pause_command,
    stop=config.stop_command,
    resume=config.resume_command,
    status=config.status_command,
    info=config.info_command,
    help=config.help_command)

REGULAR_HELP_MESSAGE = u"""
{code} : Вбить один код целиком. Пример: {code} один длинный код
{codes} : Вбить несколько кодов, разделённых пробелом. Пример: {codes} код1 код2 код3
{task} : Повторно вывести текущее задание
{hints} : Повторно вывести список всех подсказок
{status} : Показать текущий статус бота
{help} : Вывести помощь
""".format(
    code=config.code_command[0],
    codes=config.codes_command[0],
    task=config.task_command,
    hints=config.hints_command,
    status=config.status_command,
    help=config.help_command)
