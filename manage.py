from logging import config as logging_config

import click

import settings
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

    updater.start_polling()
    updater.idle()


@cli.command(short_help='init db')
def init_db():
    create_db(DbConfig.sqlite_db_name)


if __name__ == '__main__':
    cli()
