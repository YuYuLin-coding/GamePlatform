import logging

import colorlog

from config import Config
log_colors = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red,bg_white',
}

RUN_MODE = Config.RUN_MODE

class Logger:

    def __init__(self, name):
        log_format = (
            "%(asctime)s - "
            "%(name)s - "
            "%(levelname)s - "
            "%(message)s"
        )

        colorlog_format = (
            "%(log_color)s" + log_format
        )

        # 使用ColoredFormatter
        formatter = colorlog.ColoredFormatter(colorlog_format, log_colors=log_colors)

        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        self.logger = logging.getLogger(name)
        
        if RUN_MODE == 'dev':
            self.logger.setLevel(logging.DEBUG)
        elif RUN_MODE == 'product':
            self.logger.setLevel(logging.INFO)
        self.logger.addHandler(handler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)
