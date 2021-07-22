import datetime
from logging import config as logging_config

import click

import settings
from chat_bot.workers import worker_today, worker_schedule
from db.create_db import create_db
from helpers.settings_reader import SettingsReader
from settings import DbConfig, LogsConfig, TgBotConfig
from telegram.ext import Updater

from chat_bot.handlers import setup_dispatcher


@click.group()
def cli():
    """Init event loop, logging config etc."""
    logging_config.dictConfig(LogsConfig.LOGGING)


@cli.command(short_help='start app')
def start():
    """Print to console application settings that are imported on __init__.py."""
    click.echo('Application settings:\n')
    SettingsReader(settings_module=settings).print_settings(print_func=click.echo)

    updater = Updater(TgBotConfig.TOKEN)

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    j = updater.job_queue
    j.run_daily(worker_schedule, days=(0, 1, 2, 3, 4, 5, 6), time=datetime.time(hour=6, minute=59, second=00))
    j.run_daily(worker_today, days=(0, 1, 2, 3, 4, 5, 6), time=datetime.time(hour=7, minute=00, second=00))

    updater.start_polling()
    updater.idle()


@cli.command(short_help='init db')
def init_db():
    create_db(DbConfig.sqlite_db_name)


if __name__ == '__main__':
    cli()
