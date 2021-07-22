from datetime import datetime

from telegram.ext import CommandHandler, MessageHandler, Filters

from chat_bot.constants import DATE_FORMAT
from chat_bot.repo import BotRepo
from settings.bot import TgBotConfig
from helpers.utils import set_reviewers, get_reviewers_list


def start(update, _):
    update.message.reply_text(TgBotConfig.WELCOME_MESSAGE)


def schedule(update, context):
    chat_id = update.effective_chat.id

    if update.effective_chat.type == 'private':
        context.bot.send_message(
            chat_id=chat_id,
            text=TgBotConfig.PRIVATE_CHAT,
        )
    else:
        set_reviewers(chat_id, context)


def today(update, context):
    chat_id = update.effective_chat.id

    if update.effective_chat.type == 'private':
        context.bot.send_message(
            chat_id=chat_id,
            text=TgBotConfig.PRIVATE_CHAT,
        )

    else:
        get_reviewers_list(context, chat_id)


def add_me(update, context):
    chat_id = update.effective_chat.id
    user = update.message.from_user
    if update.effective_chat.type == 'private':
        context.bot.send_message(
            chat_id=chat_id,
            text=TgBotConfig.PRIVATE_CHAT,
        )
    else:
        with BotRepo() as bot_repo:
            bot_repo.add_user(
                user_id=user.id,
                username=user.username,
                chat_id=chat_id
            )

            context.bot.send_message(
                chat_id=chat_id,
                text=TgBotConfig.ADD_ME.format(
                    f_name=user.first_name,
                    s_name=user.last_name
                ),
            )

            set_reviewers(chat_id, context)


def stop_me(update, context):
    chat_id = update.effective_chat.id
    user = update.message.from_user

    if update.effective_chat.type == 'private':
        context.bot.send_message(
            chat_id=chat_id,
            text=TgBotConfig.PRIVATE_CHAT,
        )
    else:
        with BotRepo() as bot_repo:
            bot_repo.mute_user(
                user_id=user.id,
            )

            context.bot.send_message(
                chat_id=chat_id,
                text=TgBotConfig.STOP_ME.format(
                    f_name=user.first_name,
                    s_name=user.last_name
                ),
            )

        set_reviewers(chat_id, context)


def help(update, context):
    chat_id = update.effective_chat.id

    context.bot.send_message(
        chat_id=chat_id,
        text="""/start - Не знаю зачем, так принято
/schedule - Сгенерировать расписание ревьюверов на ближайшие 14 дней
/today - Кто сегодня на ревью?

/add_me - Добавь меня в список ревьюверов
/stop_me - Не добавляй меня в список ревьюверов (! не забудьте нажать при уходе в отпуск или болезни)

Еще слежу за вами в чате и отсылаю МР текущим ревьюеверам
        """
    )


def find_mr(update, context):
    today = datetime.now().strftime(DATE_FORMAT)
    with BotRepo() as bot_repo:
        users = bot_repo.get_reviewers(date=today, chat_id=update.effective_chat.id)
        user_ids = [user[1] for user in users]
        for user in user_ids:
            try:
                update.message.forward(chat_id=user)
            except Exception: #todo delete it, for test
                continue


def setup_dispatcher(dp):
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('schedule', schedule))
    dp.add_handler(CommandHandler('today', today))

    dp.add_handler(CommandHandler('add_me', add_me))
    dp.add_handler(CommandHandler('stop_me', stop_me))

    dp.add_handler(MessageHandler(Filters.regex('https://scm.x5.ru/') & Filters.regex('merge_requests'), find_mr))

    # dp.add_handler(MessageHandler(Filters.chat_type.private, forward_to_chat))
    # dp.add_handler(MessageHandler(Filters.chat(TgBotConfig.TELEGRAM_SUPPORT_CHAT_ID) & Filters.reply, forward_to_user))
    return dp
