# Makes the given text colored and return the colored text

# DEBUG = True
DEBUG = False


def fail(message):
    _FAIL = "\033[91m"
    _ENDC = "\033[0m"
    print("HATA! " + _FAIL + message + _ENDC)


def warning(message):
    _WARNING = "\033[93m"
    _ENDC = "\033[0m"
    print("UYARI!" + _WARNING + str + _ENDC)


def verbose(message):
    print("INFO:" + message)


def debug(message):
    if DEBUG:
        print("UUT: " + message)
