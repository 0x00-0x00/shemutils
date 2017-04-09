import time


class Timer(object):
    """
    Timer object to track periods of time.
    """

    def __init__(self):
        self.start = time.time()
        self.stop = None

    def _rearm(self):
        self.start = time.time()
        self.stop = None
        return 0

    def stop(self):
        """
        Set a stop time if not set, then calculate the elapsed time and
        returns the formatted elapsed time in String data type, totally human-
        readable.
        """
        if self.stop is None:
            self.stop = time.time()
        elapsed = self.stop - self.start
        self._rearm()  # rearm the class for re-use
        return self.format_time(elapsed)

    @staticmethod
    def format_time(t):
        if t > 86400:
            days = (t / 86400)
            hours = (t % 86400) / 3600
            minutes = (t % 3600) / 60
            seconds = ((t % 86400) % 3600) % 60
            return "%2.fd %2.fh %2.fm %2.fs" % (days, hours, minutes, seconds)
        elif t > 3600:
            hours = (t / 3600.0)
            minutes = ((t % 3600) / 60)
            seconds = ((t % 3600) % 60)
            return "%2.fh %2.fm %2.fs" % (hours, minutes, seconds)
        elif t > 60:
            minutes = (t / 60)
            seconds = (t % 60)
            return "%2.fm %2.fs" % (minutes, seconds)
        else:
            seconds = t
            return "%2.fs" % seconds
