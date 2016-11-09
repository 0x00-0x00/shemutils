import os
import hashlib


class Checksum(object):
    """
    to use this class you need to pass a valid path and a string or int denoting a valid hash algorithm

    examples:
    checksum = Checksum("file.pdf", 0) or Checksum("file.pdf", "md5")
    """
    def __init__(self, filename, algorithm):
        self.file = filename
        self.algorithm = algorithm

    def _check(self):
        if not os.path.isfile(self.file):
            return -1
        else:
            return 0

    def _readnhash(self, algorithm, chunk=4096):
        if algorithm == 0 or algorithm == "md5":
            m = hashlib.md5()
        elif algorithm == 1 or algorithm == "sha256":
            m = hashlib.sha256()
        elif algorithm == 2 or algorithm == "sha512":
            m = hashlib.sha512()
        elif algorithm == 3 or algorithm == "sha1":
            m = hashlib.sha1
        else:
            return -1
        with open(self.file, "rb") as f:
            while True:
                data = f.read(chunk)
                if not data:
                    break
                m.update(data)
        return m.hexdigest()

    def get(self):
        if self._check() < 0:
            return -1
        return self._readnhash(algorithm=self.algorithm)

