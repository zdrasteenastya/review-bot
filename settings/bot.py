from settings.base import env


class TgBotConfig(object):
    TOKEN = env.str('TG_TOKEN', default='1888295997:AAEjCbO7IERnA4u1BhXMa1GhocF3QwEX9XQ')
    CHAT_ID_FOR_WORKERS = '-440211705'
    WELCOME_MESSAGE = 'День добрый :)'
    EVERY_DAY_TEXT = 'По МР сегодня: @{user_1} и @{user_2}'
    ADD_ME = 'Запомнил тебя, {f_name} {s_name}'
    STOP_ME = 'До новых встреч и удачи тебе, {f_name} {s_name}. Сейчас переделаю расписание \U0001F612'
    EMPTY_SCHEDULE = 'Нет расписания на сегодня'
    NOT_ENOUGH_REVIEWERS = 'Вас слишком мало, ты один, сам свои МР смотри :)'
    PRIVATE_CHAT = 'Это развитие нашей бесседы бессмысленно'
