from typing import TYPE_CHECKING
from os.path import exists, join
from os import getcwd
from tkinter.filedialog import askdirectory
try:
    from pwinput import pwinput as getpass
except:
    from getpass import getpass

from src import logger
from src.argv_handler import get_args
from src.login import login

if TYPE_CHECKING:
    from requests import Session

BASE_PATH: str = None
FIRST_RUN: bool = None
SESSION: Session = None
ARGV: dict = None


def init_globals():
    global BASE_PATH, FIRST_RUN, SESSION, ARGV
    ARGV = get_argv_dict()
    BASE_PATH = get_directory()
    FIRST_RUN = get_first_run()
    SESSION = get_session()


def get_argv_dict():
    """
    Returns command line arguments as python dict
    """
    return get_args(d=1, u=2, debug=0, verbose=0)

def get_directory():
    """
    Gets the directory from command line if exists, else shows a folder dialog\n
    Guarantees that the returned path exists, if the path does not exists than exits with error\n
    Accesses to '.last_dir' file to get last used directory
    """

    # Get last selected directory from file
    try:
        default_dir_file = open(join(getcwd(), ".last_dir"), "r")
        default_dir = default_dir_file.read().strip()
    except:
        default_dir = getcwd()
    finally:
        default_dir_file.close()

    if "d" in ARGV:
        if exists(ARGV["d"][0]):
            # Get download directory from command line
            download_directory = ARGV["d"][0]
        else:
            logger.warning(
                f"-d parametresi ile verilen {ARGV['d'][0]} klasörü bulunamadı."
            )
            download_directory = askdirectory(
                initialdir=default_dir, title="Ninova Arşivci - İndirme klasörü seçin"
            )
    else:
        download_directory = askdirectory(
            initialdir=default_dir, title="Ninova Arşivci - İndirme klasörü seçin"
        )

    if not exists(download_directory):
        logger.fail(f"Verilen '{download_directory}' geçerli bir klasör değil!")

    try:
        default_dir_file = open(join(getcwd(), ".last_dir"), "w")
        default_dir_file.write(download_directory)
    finally:
        default_dir_file.close()

    return download_directory

def get_first_run():
    """
    Checks whether this is the first time that program ran on selected directory by checking database file
    """
    if BASE_PATH:
        first_run = not exists(join(BASE_PATH, "ninova_arsivci.db"))
        return first_run
    else:
        logger.fail("Klasör seçilmemiş. get_directory() fonksiyonu ile BASE_PATH değişkeni ayarlanmalı!")

def get_session():
    """
    Gets username and password from commandline if exists, else prompts user\n
    Eğer kullanıcı adı veya şifre yanlış se
    """
    while True:
        if "u" in ARGV:
            username, password = ARGV["u"]
        else:
            username = input("Kullanıcı adı (@itu.edu.tr olmadan): ")
            password = getpass("Şifre: ")
    
        try:
            session = login( (username, password) )
            return session
        except:
            try:
                del ARGV["u"]
            except:
                pass
            logger.warning("Kullanıcı adı veya şifre hatalı. Tekrar deneyin.")

