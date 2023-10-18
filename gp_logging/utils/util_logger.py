import logging
import colorlog

class CustomLogger:

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

        colorlog.basicConfig(level=logging.DEBUG, format=colorlog_format)

        self.logger = logging.getLogger(name)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)

    # If needed, you can further add methods like log_warning, log_debug, etc.
