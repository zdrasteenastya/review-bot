from datetime import datetime

from chat_bot.constants import DATE_FORMAT
from chat_bot.repo import BotRepo
from helpers.utils import get_reviewers_list, set_reviewers
from settings import TgBotConfig


def worker_today(context):
    chat_id = TgBotConfig.CHAT_ID_FOR_WORKERS
    get_reviewers_list(context, chat_id)


def worker_schedule(context):
    chat_id = TgBotConfig.CHAT_ID_FOR_WORKERS
    today = datetime.now().strftime(DATE_FORMAT)

    with BotRepo() as bot_repo:
        schedule = bot_repo.get_reviewers(date=today, chat_id=chat_id)
        if not schedule:
            set_reviewers(chat_id, context)
