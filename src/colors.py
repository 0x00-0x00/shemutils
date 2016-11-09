class Colors:
    purple1 = '\033[95m'
    light_blue1 = '\033[94m'
    green1 = '\033[92m'
    yellow1 = '\033[93m'
    light_red1 = '\033[91m'
    end = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'
    black1 = '\033[97m'
    grey1 = '\033[90m'
    bg_red1 = '\033[41m'
    bg_green = '\033[42m'
    bg_yellow = '\033[43m'
    bg_blue = '\033[44m'
    bg_pink = '\033[45m'
    bg_grey = '\033[47m'
    bg_lgrey = '\033[7m'


def green(message):
    return Colors.green1 + message + Colors.end


def blue(message):
    return Colors.light_blue1 + message + Colors.end


def yellow(message):
    return Colors.yellow1 + message + Colors.end


def red(message):
    return Colors.light_red1 + message + Colors.end


def bold(message):
    return Colors.bold + message + Colors.end


def underline(message):
    return Colors.underline + message + Colors.end
