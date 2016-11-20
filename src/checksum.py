import os
import hashlib
import gevent

from logger import Logger
from colors import *


class Checksum(object):
    """
    to use this class you need to pass a valid path and a string or int denoting a valid hash algorithm

    examples:
    checksum = Checksum("file.pdf", 0) or Checksum("file.pdf", "md5")
    """
    def __init__(self, filename, algorithm, verbose=True):
        self.file = filename
        self.algorithm = algorithm
        self.verbose = verbose
        self.logger = Logger("Checksum")

    def _check(self):
        """Check if file supplied in class argument really exists."""
        if not os.path.isfile(self.file):
            if self.verbose:
                self.logger.critical("Could not find file '{0}'".format(self.file))
            return None
        else:
            return 0

    def _readnhash(self, algorithm, chunk=4096):
        """Detects algorithm, read file content, update into alg. object and hex digest."""
        if algorithm == 0 or algorithm == "md5":
            m = hashlib.md5()
            alg = "MD5"
        elif algorithm == 1 or algorithm == "sha256":
            m = hashlib.sha256()
            alg = "SHA256"
        elif algorithm == 2 or algorithm == "sha512":
            m = hashlib.sha512()
            alg = "SHA512"
        elif algorithm == 3 or algorithm == "sha1":
            m = hashlib.sha1
            alg = "SHA1"
        else:
            return -1

        if self.verbose:
            self.logger.info("Set hashing algorithm to {0}".format(blue(alg)))

        #  Attempts to read file and update its contents to hashing object
        #  Variables:
        #  data => holds file data
        #  n    => holds bytes read

        with open(self.file, "rb") as f:
            n = 0
            while True:
                data = f.read(chunk)
                if not data:
                    break
                m.update(data)

                #  Adds chunk size to n
                n += len(data)

        #  Returns the hexadecimal digest and filename
        if self.verbose:
            self.logger.info("Processed a total of {0} bytes from file.".format(n))
        return m.hexdigest() + "    " + "{0}".format(self.file)

    def get(self):
        """Returns the output from _readnhash() function"""
        if self._check() < 0:
            return -1
        g = gevent.spawn(self._readnhash, self.algorithm)
        g.join()
        return g.get()

