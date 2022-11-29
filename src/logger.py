# Makes the given text colored and return the colored text

from time import perf_counter

DEBUG = False
VERBOSE = False
FILE_NAME_MAX_LENGTH = 30

_FAIL = "\033[91m"
_ENDC = "\033[0m"
_WARNING = "\033[93m"
_GREEN = '\033[92m'

def enable_debug():
    global DEBUG
    DEBUG = True

def enable_verbose():
    global VERBOSE
    VERBOSE = True

def fail(message):
    print("HATA! " + _FAIL + message + _ENDC)
    exit()


def warning(message):
    print("UYARI!" + _WARNING + message + _ENDC)


def verbose(message):
    if VERBOSE:
        print("INFO: " + message)

def new_file(file_path):
    print(_GREEN + "Yeni: " + file_path + _ENDC)


def debug(message):
    if DEBUG:
        print("UUT:  " + message)


def speed_measure(debug_name: str, is_level_debug: bool, return_is_debug_info: bool = False):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = perf_counter()
            return_val = func(*args, **kwargs)
            end = perf_counter()
            
            additional_info = return_val[0] if return_is_debug_info else ""

            if is_level_debug:
                debug(f"{additional_info[:FILE_NAME_MAX_LENGTH]:<30} {debug_name} {end-start} saniyede tamamlandı.")
            else:
                verbose(f"{additional_info[:FILE_NAME_MAX_LENGTH]:<30} {debug_name} {end-start} saniyede tamamlandı.")


            return return_val
    
        return wrapper
    return decorator
