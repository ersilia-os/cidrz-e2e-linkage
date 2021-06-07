import sys
import os
from loguru import logger
from ..vars import E2ELINK_DIR, LOGGING_FILE


ROTATION = "10 MB"


class Logger(object):
    def __init__(self):
        self.logger = logger
        self.logger.remove()
        self._console = None
        self._file = None
        self._log_to_file()
        self._log_to_console()

    def _log_to_file(self):
        self._file = self.logger.add(
            os.path.join(E2ELINK_DIR, LOGGING_FILE), rotation=ROTATION
        )

    def _log_to_console(self):
        if self._console is None:
            self._console = self.logger.add(sys.stderr)

    def _unlog_from_console(self):
        if self._console is not None:
            self.logger.remove(self._console)
            self._console = None

    def set_verbosity(self, verbose):
        if verbose:
            self._log_to_console()
        else:
            self._unlog_from_console()

    def debug(self, text):
        self.logger.debug(text)

    def info(self, text):
        self.logger.info(text)

    def warning(self, text):
        self.logger.warning(text)

    def error(self, text):
        self.logger.error(text)

    def critical(self, text):
        self.logger.critical(text)

    def success(self, text):
        self.logger.success(text)


logger = Logger()
