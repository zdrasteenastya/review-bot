import json
import sqlite3

import psycopg2

from chat_bot import queries
from chat_bot.constants import USERS_FILE, SCHEDULE_FILE
from settings import DbConfig


class BotRepo():
    def __init__(self):
        self.db_conn = sqlite3.connect(DbConfig.sqlite_db_name)
        self.cursor = self.db_conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
        self.db_conn.close()

    def create_schedule(self, rows):
        records_list_template = ','.join(['%s'] * len(rows))
        self.cursor.execute(queries.insert_schedule.format(records_list_template), rows)
        self.db_conn.commit()

    def delete_old_schedule(self):
        self.cursor.execute(queries.truncate_schedule)
        self.db_conn.commit()

    def get_reviewers(self, date, chat_id):
        self.cursor.execute(queries.get_reviewers.format(rw_date=date, chat_id=chat_id))
        users = self.cursor.fetchall()
        return users

    def add_user(self, user_id, username, chat_id):
        self.cursor.execute(queries.insert_user.format(
            user_id=user_id,
            username=username,
            chat_id=chat_id
        ))
        self.db_conn.commit()

    def get_reviewers_list(self, chat_id):
        self.cursor.execute(queries.select_reviewers.format(chat_id=chat_id))
        usernames = self.cursor.fetchall()
        return [username[0] for username in usernames]

    def mute_user(self, user_id):
        self.cursor.execute(queries.update_user.format(user_id=user_id))
        self.db_conn.commit()

#
# class FileRepo():
#     def __init__(self):
#         self.users_file = open(USERS_FILE, 'r+')
#         self.schedule_file = open(SCHEDULE_FILE, 'r+')
#
#         self.users = json.loads(self.users_file.read())
#         self.schedule = json.loads(self.schedule_file.read())
#
#         self.users_file.seek(0)
#         self.schedule_file.seek(0)
#
#     def __enter__(self):
#         return self
#
#     def __exit__(self, exc_type, exc_value, traceback):
#         self.users_file.close()
#         self.schedule_file.close()

    # def create_schedule(self, rows):
    #     records_list_template = ','.join(['%s'] * len(rows))
    #     self.cursor.execute(queries.insert_schedule.format(records_list_template), rows)
    #     self.db_conn.commit()
    #
    # def delete_old_schedule(self):
    #     self.cursor.execute(queries.truncate_schedule)
    #     self.db_conn.commit()

    # def get_reviewers(self, date, chat_id):
    #     self.cursor.execute(queries.get_reviewers.format(rw_date=date, chat_id=chat_id))
    #     users = self.cursor.fetchall()
    #     return users
    #
    # def add_user(self, user_id, username, chat_id):
    #     chat_info = self.users.get(chat_id)
    #     user_info = {
    #         user_id: {
    #             'username': username,
    #             'muted': False
    #         }
    #     }
    #     if not chat_info:
    #         self.users[chat_id] = [user_info]
    #     else:
    #         self.users[chat_id].append(user_info)
    #
    #     self.users_file.write(json.dumps(self.users))

    # def get_reviewers_list(self, chat_id):
    #     self.cursor.execute(queries.select_reviewers.format(chat_id=chat_id))
    #     usernames = self.cursor.fetchall()
    #     return [username[0] for username in usernames]
    #
    # def mute_user(self, user_id):
    #     self.cursor.execute(queries.update_user.format(user_id=user_id))
    #     self.db_conn.commit()
