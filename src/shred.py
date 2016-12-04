import os
import time
from logger import Logger


class Shredder(object):
    """
    Shredder class written by shemhazai
    """
    def __init__(self, chunk_size=1024):
        self.logger = Logger("Shredder")
        self.chunk_size = chunk_size

    def _get_blocks(self, size):
        """
        Calculates how many chunks (or blocks) are going to be used in the shredding process
        :param size: int for file size
        :return: list with byte length for each block
        """
        blocks = []
        n = size / self.chunk_size  # full-sized chunks
        r = size % self.chunk_size  # last chunk size
        for k in range(n):
            blocks.append(self.chunk_size)
        blocks.append(r)  # append the last block
        return blocks

    @staticmethod
    def _generate_random_block(size):
        return os.urandom(size)

    @staticmethod
    def _getsize(f):
        return os.path.getsize(f)

    def shred(self, f, v=False):
        """
        Function to shred files
        :param f: string file name
        :param v: verbose boolean
        :return: bytes overwritten
        """

        file_size = self._getsize(f)
        if v is True:
            self.logger.debug("File size: {0}".format(file_size))

        blocks = self._get_blocks(file_size)
        if v is True:
            self.logger.debug("Generated {0} blocks of 1kb".format(len(blocks)))

        try:
            file_handle = open(f, "wb")
            if v is True:
                self.logger.debug("File handle open.")
        except Exception as e:
            self.logger.error("ERROR: {0}".format(e))
            return -1

        t1 = time.time()  # track init time
        overwritten = 0  # track overwritten bytes
        for block in blocks:
            file_handle.write(self._generate_random_block(block))  # write random data into file
            overwritten += block
            #  possibility to print percentage here.
        t2 = time.time()  # track end time
        if v is True:
            self.logger.debug("Shredding took {0} seconds.".format(t2-t1))
        return overwritten
