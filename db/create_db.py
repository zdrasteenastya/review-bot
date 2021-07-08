import sqlite3

from settings import DbConfig
from .queries import create_schedule, create_users


def create_db(db_name):
    sqlite_connection = sqlite3.connect(db_name)
    try:
        cursor = sqlite_connection.cursor()
        print("База данных подключена к SQLite")
        cursor.execute(create_schedule)
        print("Таблица расписания создана")
        cursor.execute(create_users)
        sqlite_connection.commit()
        print("Таблица пользователей создана")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
