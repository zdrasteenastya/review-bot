from aiohttp.web_log import AccessLogger
from settings import LogsConfig


class CustomAccessLogger(AccessLogger):

    def log(self, request, *args, **kwargs):
        if request.path in LogsConfig.UNLOG_PATH:
            return
        if LogsConfig.ACCESS_LOG:
            super().log(request, *args, **kwargs)
