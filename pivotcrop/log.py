"""Basic CLI logging utils.
"""
# pylint: disable=too-few-public-methods

import sys
from dataclasses import dataclass


class Verbosity(int):
    """Defines log verbosity settings."""
    ERROR = 0
    WARNING = 1
    INFO = 2
    DEBUG = 3


class BColors:
    """Defines colors for terminal text."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


@dataclass
class Logger:
    """Utility class for verbosity based logging."""
    verbosity: Verbosity = Verbosity.INFO

    def debug(self, msg: str):
        """Debug message."""
        if self.verbosity >= Verbosity.DEBUG:
            print(msg)

    def info(self, msg: str):
        """Info message."""
        if self.verbosity >= Verbosity.INFO:
            print(msg)

    def success(self, msg: str):
        """Success message."""
        if self.verbosity >= Verbosity.INFO:
            print(BColors.OKGREEN + msg + BColors.ENDC)

    def warning(self, msg: str):
        """Warning message."""
        if self.verbosity >= Verbosity.WARNING:
            print(BColors.WARNING + msg + BColors.ENDC)

    def error(self, msg: str):
        """Warning message."""
        if self.verbosity >= Verbosity.ERROR:
            print(BColors.FAIL + msg + BColors.ENDC, file=sys.stderr)
