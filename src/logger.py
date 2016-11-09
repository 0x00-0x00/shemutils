import os
import logging
from colors import *


class Logger:
    def __init__(self, logger_name):
        """Logging module wrapper to easily encapsulate code for re-use in my own projects."""
        self.logger_name = logger_name
        self.operational_system = os.name
        self.color_flag = self.set_color_flag()
        self.loggerHandle = self._create_logger()
        self.consoleHandle = self._create_console()
        self.formatter = self._create_formatter()
        self.define_logger_level([self.loggerHandle, self.consoleHandle])
        self.consoleHandle.setFormatter(self.formatter)
        self.loggerHandle.addHandler(self.consoleHandle)

    def set_color_flag(self):
        return True if self.operational_system == "posix" else False

    def define_logger_level(self, objs):
        return [self._set_level(x) for x in objs]

    def _create_logger(self):
        return logging.getLogger(self.logger_name)

    @staticmethod
    def _create_console():
        return logging.StreamHandler()

    @staticmethod
    def _create_formatter():
        return logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s", "%H:%M:%S")

    @staticmethod
    def _set_level(logger_obj, level=logging.DEBUG):
        return logger_obj.setLevel(level)

    def success(self, string):
        if self.color_flag:
            self.loggerHandle.info(green("[^] ") + string)
        else:
            self.loggerHandle.info(string)
        return

    def step_ok(self, string):
        max_len = 32
        diff = max_len - len(string)
        if self.color_flag:
            self.loggerHandle.info("{0} ".format(string) + " ".rjust(diff, ".") + ": " + green("SUCCESS"))
        else:
            self.loggerHandle.info("{0} ".format(string) + " ".rjust(diff, ".") + ": " + "SUCCESS")

    def step_fail(self, string):
        max_len = 32
        diff = max_len - len(string)

        if self.color_flag:
            self.loggerHandle.info("{0} ".format(string) + " ".rjust(diff, ".") + ": " + red("FAILED"))
        else:
            self.loggerHandle.info("{0} ".format(string) + " ".rjust(diff, ".") + ": " + "FAILED")

    def info(self, string):
        if self.color_flag:
            self.loggerHandle.info(blue("[*] ") + string)
        else:
            self.loggerHandle.info(string)
        return

    def debug(self, string):
        if self.color_flag:
            self.loggerHandle.debug(yellow("[#] ") + string)
        else:
            self.loggerHandle.debug(string)
        return

    def warning(self, string):
        if self.color_flag:
            self.loggerHandle.warning(yellow("[!] ") + string)
        else:
            self.loggerHandle.warning(string)
        return

    def error(self, string):
        if self.color_flag:
            self.loggerHandle.error(red("[@] ") + string)
        else:
            self.loggerHandle.error(string)
        return

    def critical(self, string):
        if self.color_flag:
            self.loggerHandle.critical(red("[!!] ") + string)
        else:
            self.loggerHandle.critical(string)
        return
