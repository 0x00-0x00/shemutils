import re
import os
import shemutils


class ConfigParser(object):
    """
    Class to return data extracted from configuration files.
    """
    def __init__(self, filename):
        self.logger = shemutils.Logger("Config-Parser")
        self.filename = self._is_valid_file(filename)
        self.data = self._start()

    def _start(self):
        if not self.filename:
            self.logger.error("Could not open configuration file")
            return None
        else:
            with open(self.filename, "r") as f:
                data = f.read()
            return self._get_configuration(data)

    @staticmethod
    def _is_valid_file(filename):
        return filename if os.path.exists(filename) else None

    @staticmethod
    def _get_configuration(data):
        pattern = "(?P<config_var>[a-z_]+)\s?=\s?(?P<value>[aA-zZ~\/\.]+)"
        m = re.match(pattern, data)
        if m is not None:
            return m.groupdict()
        else:
            return None
