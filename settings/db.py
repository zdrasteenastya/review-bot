from .base import env


class DbConfig(object):
    sqlite_db_name = env.str('DB_NAME', default='sqlite_python.db')