import sys

from helpers.logging.formatters import JSONFormatter

from .base import DEBUG, ROLE, env


class LogsConfig(object):
    LOG_LEVEL = env.str('LOG_LEVEL', default='DEBUG')
    UNLOG_PATH = ('/readiness', '/liveness')
    ACCESS_LOG = env.bool('LOGGING_ACCESS_LOG', default=True)
    LOGGING = dict(  # noqa:C408. Ignore Unnecessary dict call there
        version=1,
        disable_existing_loggers=False,
        loggers={
            '': {
                'level': LOG_LEVEL,
                'handlers': ['console'],
            },
            'root': {
                'level': 'DEBUG' if DEBUG else LOG_LEVEL,
                'handlers': ['console'],
                'propagate': False,
            },
            'envparse': {
                'level': 'ERROR',
            },
        },
        handlers={
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'generic' if ROLE == 'local' else 'json',
                'stream': sys.stdout,
            },
            'error_console': {
                'class': 'logging.StreamHandler',
                'formatter': 'generic',
                'stream': sys.stderr,
            },
            'access_console': {
                'class': 'logging.StreamHandler',
                'formatter': 'access',
                'stream': sys.stdout,
            },
        },
        formatters={
            'generic': {
                'format': '%(asctime)s (%(name)s)[%(levelname)s] %(message)s',
                'datefmt': '[%Y-%m-%d %H:%M:%S %z]',
                'class': 'logging.Formatter',
            },
            'access': {
                'format': '%(asctime)s - (%(name)s)[%(levelname)s]: ' + '%(request)s %(message)s %(status)d %(byte)d',
                'datefmt': '[%Y-%m-%d %H:%M:%S %z]',
                'class': 'logging.Formatter',
            },
            'json': {
                '()': JSONFormatter,
                'jsondumps_kwargs': {
                    'ensure_ascii': False,
                },
            },
        },
    )
