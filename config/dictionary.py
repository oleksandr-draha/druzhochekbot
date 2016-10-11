# -*- coding: utf-8 -*-
from config import config

TASK_APPEND = unichr(55356) + unichr(57152)
HINTS_APPEND = unichr(55356) + unichr(57119)
RIGHT_APPEND = unichr(55357) + unichr(56474)
WRONG_APPEND = unichr(55357) + unichr(56468)
LIMIT_APPEND = unichr(55357) + unichr(56489)
ORG_MESSAGE_APPEND = unichr(55357) + unichr(56803)

PAUSED_MESSAGES = [u'Я на паузе.',
                   u'Серьёзно, я пока не буду коды вбивать.',
                   u'Ты слышишь? Коды не вбиваю, задания не присылаю',
                   u'Алё, гараж? Ты или запусти меня или хватит слать тут.',
                   u'Я ща реально обижусь',
                   u'Ох ну ты и тугой.',
                   u'Всё. Ничего не делаю']
ALREADY_PAUSED_MESSAGES = [u'Я и так на паузе.',
                           u'Не поверишь. Я и так давно на паузе',
                           u'Чё ты хочешь? На паузе я']
RESUME_MESSAGES = [u'Я тебя сейчас наверное удивлю, но я и так работаю.',
                   u'Прикинь, да, вот просто так можешь отсылать коды и всё будет ок.',
                   u'Ну хватит уже, нечем другим заняться больше? Давай, работай',
                   u'Ох ну ты и тугой.',
                   u'Я и так работаю']
GREETINGS_MESSAGES = [u"Привет! Я твой дружочек. Соскучился? А я да.",
                      u"Здравствуй, дорогой! Как дела?",
                      u"Приветули",
                      u"Оп-па, какие люди!",
                      ]
BYE_MESSAGES = [u"Всё, давай, пока!",
                u"Давай, до свидания!",
                u"До скорых встреч, уважаемый.",
                u"Спасибо, пойду спать."]
AFFIRMATIVE_MESSAGES = [u"Я понял тебя, братан",
                        u"Замётано",
                        u"Так точно"]
UNKNOWN_MESSAGES = [u"Я тебя не понимаю"]
NOT_GROUP_CHAT_MESSAGES = [u"Напиши мне в групповом чате, а не в личку."]
START_PAUSE_MESSAGES = [u"Отдохну немного.",
                        u"Ну пауза так пауза",
                        u"Так. Не трогаю пока ничего тут",
                        ]
END_PAUSE_MESSAGES = [u"Так, продолжаем.",
                      u"И снова здравствуйте!",
                      u"Бот возобновил работу.",
                      ]
LETS_GO_MESSAGES = [u"Ну всё, погнали!",
                    u"Поехали!",
                    u"Воо-оо-оойтии-ии-и в игруу-уу-уу"]
DISAPPROVE_MESSAGES = [u"Что-то мне они не нравятся. Не буду пока их слушать."]
NO_CODE_FOUND_MESSAGE = u'_Нет кодов для вбития. Попробуй ещё раз. Формат: /c code1 code2_'
WRONG_CODE_MESSAGE = u'Неверный код!'
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
ACCESS_VIOLATION_MESSAGES = [
    u"*Данная операция запрещена для вас, уважаемый.*",
]
NO_GROUP_CHAT_MESSAGES = [
    u"Я не хочу при незнакомых людях. Давай в личку."
]
NOT_FOR_GROUP_CHAT_MESSAGES = [
    u"Ну не при всех же. Давай в личку."
]

STATUS_MESSAGE = u"Статус дружочка: {paused}\r\n" \
                 u"Активная группа: {chat_id}\r\n" \
                 u"Соединение к игровому серверу: {game_connection}\r\n" \
                 u"Текущий номер задания: {game_level_id}\r\n" \
                 u"Показанные подсказки: {game_hint_id}\r\n"
INFO_MESSAGE = u"Логин: {login}\r\n" \
               u"Пароль: {password}\r\n" \
               u"Хост: {host}\r\n" \
               u"Игра: {game_id}\r\n"
BOT_WAS_RESET_MESSAGE = u"Состояние бота было сброшено на начальное."

PAUSED_STATUS_MESSAGES = {False: u"Активный",
                          True: u"На паузе"}

GAME_CONNECTION_MESSAGES = {True: u"Активно",
                            False: u"Ошибка"}
TASK_MESSAGE = u'<b>---------------------------</b>\r\n' \
               u'<b>Задание {level_number}</b>\r\n' \
               u'<b>---------------------------</b>\r\n' \
               u'\r\n{task}'
NEW_TASK_MESSAGE = u'{smile}<b>Новый уровень!</b>\r\n' \
                   u'{task}'.format(smile=TASK_APPEND, task=TASK_MESSAGE)
NEW_HINT_MESSAGE = u'{smile}<b>Новая подсказка!</b> \r\n' \
                   u'<b>---------------------------</b>\r\n' \
                   u'<b>Подсказка {hint_number}</b>\r\n' \
                   u'<b>---------------------------</b>\r\n' \
                   u'\r\n' \
                   u'\r\n {hint}'
TASK_EDITED_MESSAGE = u'<b>Задание было изменено!</b> \r\n' \
                      u'<b>---------------------------</b>\r\n' \
                      u'\r\n' \
                      u'\r\n{task}'

CODES_LEFT_TEXT = {1: u'<b>Остался {codes} код!</b>',
                   2: u'Осталось {codes} кода!',
                   3: u'Осталось {codes} кода!',
                   4: u'Осталось {codes} кода!',
                   'all': u'Осталось {codes} кодов!'}

ADMIN_HELP_MESSAGE = u"""
{code} : Вбить код целиком. Пример: {code} один длинный код
{codes} : Вбить несколько кодов, разделённых пробелом. Пример: {codes} код1 код2 код3
{task} : Повторно вывести текущее задание
{hints} : Повторно вывести список всех подсказок
{approve} : Добавить чат в список доверенных
{disapprove} : Удалить чат из списка доверенных
{edit} : Изменить текущие настройки бота
{save} : Перезаписать настройки бота по-умолчанию
{reset} : Сбросить состояние бота в изначальное
{pause} : Прекратить отслеживание заданий и вбитие кодов
{resume} : Возобновить отслеживание заданий и вбитие кодов
{stop} : Закончить работу с ботом
{status} : Показать текущий статус бота
{info} : Вывести детальную информацию о настройках бота
{help} : Вывести помощь
""".format(
    code=config.code_command[0],
    codes=config.codes_command[0],
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
{code} : Вбить код целиком. Пример: {code} один длинный код
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
