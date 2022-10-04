# Makes the given text colored and return the colored text
import logging


def fail(message):
    _FAIL = "\033[91m"
    _ENDC = "\033[0m"
    logging.critical(_FAIL + message + _ENDC)


def warning(message):
    _WARNING = "\033[93m"
    _ENDC = "\033[0m"
    logging.warning(_WARNING + str + _ENDC)


def verbose(message):
    logging.info(message)


def debug(message):
    logging.debug(message)
