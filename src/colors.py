class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def green(message):
    return Colors.OKGREEN + message + Colors.ENDC


def blue(message):
    return Colors.OKBLUE + message + Colors.ENDC


def yellow(message):
    return Colors.WARNING + message + Colors.ENDC


def red(message):
    return Colors.FAIL + message + Colors.ENDC


def bold(message):
    return Colors.BOLD + message + Colors.ENDC


def underline(message):
    return Colors.UNDERLINE + message + Colors.ENDC
