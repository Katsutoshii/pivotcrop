"""Basic CLI logging utils.
"""
from dataclasses import dataclass


class Verbosity(int):
    ERROR = 0
    WARNING = 1
    INFO = 2
    DEBUG = 3


class BColors:
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
    verbosity: Verbosity = Verbosity.INFO

    def debug(self, input: str):
        if (self.verbosity >= Verbosity.DEBUG):
            print(input)

    def info(self, input: str):
        if (self.verbosity >= Verbosity.INFO):
            print(input)

    def success(self, input: str):
        if (self.verbosity >= Verbosity.INFO):
            print(BColors.OKGREEN + input + BColors.ENDC)

    def warning(self, input: str):
        if (self.verbosity >= Verbosity.WARNING):
            print(BColors.WARNING + input + BColors.ENDC)

    def error(self, input: str):
        if (self.verbosity >= Verbosity.ERROR):
            print(BColors.FAIL + input + BColors.ENDC)
