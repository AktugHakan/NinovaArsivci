# Makes the given text colored and return the colored text

def fail(str):
    _FAIL = '\033[91m'
    _ENDC = '\033[0m'

    return _FAIL + str + _ENDC


def warning(str):
    _WARNING = '\033[93m'
    _ENDC = '\033[0m'

    return _WARNING + str + _ENDC
