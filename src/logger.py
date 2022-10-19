# Makes the given text colored and return the colored text

from time import perf_counter

DEBUG = True

def set_debug(toDebug: bool):
    global DEBUG
    DEBUG = toDebug

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


def speed_measure(debug_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = perf_counter()
            return_val = func(*args, **kwargs)
            end = perf_counter()
                
            verbose(f"{debug_name} işlemi {end-start} saniyede tamamlandı.")

            return return_val
    
        return wrapper
    return decorator
