from datetime import datetime, timedelta
import random
from itertools import product
from time import sleep

from chat_bot.constants import REVIEWERS_COUNT, WEEKEND_DAYS, NUM_SCHEDULE_DATES, DAY_FOR_REVIEW, DATE_FORMAT, \
    DAY_OF_WEEK
from chat_bot.repo import BotRepo
from settings import TgBotConfig


def generate_schedule(list_reviewers, chat_id):
    with BotRepo() as bp:
        bp.delete_old_schedule()

    output_schedule = {}
    dates = [generate_dates(i) for i in range(NUM_SCHEDULE_DATES)]
    dates = list(filter(lambda dates: dates[1] not in WEEKEND_DAYS, dates))

    for a in range(1, len(dates) + 1, DAY_FOR_REVIEW):
        two_people = choose_random_people(list_reviewers, output_schedule)

        day_one = dates[a - 1]
        day_two = dates[a]
        output_schedule[f'{day_one[0]} {day_one[1]}'] = two_people
        output_schedule[f'{day_two[0]} {day_two[1]}'] = two_people

        with BotRepo() as bot_repo:
            # TODO: bot_repo.delete_old_schedule не работает!
            bot_repo.create_schedule(tuple(product([day_one[0], day_two[0]], two_people, [chat_id])))

    output_schedule_text = generate_text_message(output_schedule)
    return output_schedule_text


def generate_dates(time_delta):
    next_day = datetime.now() + timedelta(days=time_delta)
    date = next_day.strftime(DATE_FORMAT)
    day_of_week = next_day.strftime(DAY_OF_WEEK)
    return date, day_of_week


def generate_text_message(mapping):
    output_text = ''
    for key, value in mapping.items():
        output_text += f'{key}: @{value[0]}, @{value[1]} \n'
    return output_text


def choose_random_people(list_reviewers, output_schedule):
    two_people = random.sample(list_reviewers, REVIEWERS_COUNT)
    if len(list_reviewers) > 3 and len(output_schedule) > 1:
        while True:
            already_reviewers = list(output_schedule.values())[-1]
            if set(already_reviewers).intersection(set(two_people)):
                two_people = random.sample(list_reviewers, REVIEWERS_COUNT)
            else:
                break
    return two_people


def get_reviewers(chat_id, context):
    with BotRepo() as bot_repo:
        reviewers = bot_repo.get_reviewers_list(chat_id=chat_id)
        if len(reviewers) <= 1:
            context.bot.send_message(
                chat_id=chat_id,
                text=TgBotConfig.NOT_ENOUGH_REVIEWERS,
            )
        else:
            return reviewers
