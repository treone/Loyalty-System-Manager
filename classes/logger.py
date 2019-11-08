import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from classes.constants import APP_NAME_WITHOUT_SPACES, USER_PATH, APP_NAME_ABBR


class StreamToLogger(object):
    """Класс для записи всех stdout и stderr"""
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        """flush()"""
        pass

    def errors(self):
        """errors()"""
        pass


logging.basicConfig(format="%(module)14s(%(asctime)s):%(levelname)s %(message)s", level=logging.INFO)
formatter = logging.Formatter('%(module)14s(%(asctime)s):%(levelname)s %(message)s')

log = logging.getLogger(APP_NAME_WITHOUT_SPACES)
log.setLevel(logging.INFO)

fh = RotatingFileHandler(
    os.path.join(USER_PATH, APP_NAME_ABBR + '.log'), encoding="utf-8", maxBytes=25*1024*1024, backupCount=3)
fh.setFormatter(formatter)
log.addHandler(fh)


def reroute_output():
    """Направляем stdout и stderr в logger"""
    so = StreamToLogger(log, logging.INFO)
    sys.stdout = so

    se = StreamToLogger(log, logging.ERROR)
    sys.stderr = se
