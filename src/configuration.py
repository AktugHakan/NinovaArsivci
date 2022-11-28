from __future__ import annotations
from os.path import exists, join
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from requests import Session

from tkinter import filedialog, messagebox
import copy

try:
    from pwinput import pwinput as getpass
except:
    from getpass import getpass

try:
    from src.argv_handler import get_args
    from src.classes import User
    from src import logger
    from src.db_handler import DATABASE_FILE_NAME, DB
except ModuleNotFoundError:
    print(
        "HATA! src klasörü bulunamadı veya yeri değiştirilmiş. Programı yeniden indirin."
    )
    exit()


class Config:
    """
    Do not create an object of this class
    Use class functions and static variables instead
    Initialize with init_config method
    """

    debug: bool
    user: User
    base_path: str
    session: Session
    merge: bool
    first_run: bool
    core_count: int

    @classmethod
    def set_initial_attr(
        cls,
        debug: bool,
        user: User,
        base_path: str,
        merge: bool,
        first_run: bool,
        core_count: int,
        verbose: bool
    ):
        cls.debug = debug
        cls.user = user
        cls.base_path = base_path
        cls.merge = merge
        cls.first_run = first_run
        cls.core_count = core_count
        cls.verbose = verbose
        from src import logger

    @classmethod
    def set_session(cls, session: Session):
        cls.session = session

    @classmethod
    def get_settings_tuple(cls):
        return (
            cls.debug,
            cls.user,
            cls.base_path,
            cls.session,
            cls.merge,
            cls.first_run,
            cls.core_count,
            DB.to_add,
            DB.db_path,
            cls.verbose
        )

    @classmethod
    def load_from_tuple(cls, settings: tuple):
        cls.debug = settings[0]
        cls.user = settings[1]
        cls.base_path = settings[2]
        cls.session = settings[3]
        cls.merge = settings[4]
        cls.first_run = settings[5]
        cls.core_count = settings[6]
        DB.to_add = settings[7]
        DB.connect(settings[8])
        cls.verbose = settings[9]
        if cls.debug:
            logger.enable_debug()
        if cls.verbose:
            logger.enable_verbose()


    @classmethod
    def get_session_copy(cls):
        return copy.deepcopy(cls.session)

    @classmethod
    def get_settings_dict(cls):
        return cls.__dict__

    @classmethod
    def init(cls):
        """
        First thing to run. Get config info from various sources

        Does not initialize "session" object. Session should be created elsewhere
        and then be set using set_session method
        """
        config_dict = get_args(d=1, u=2, core=1, debug=0, verbose=0)

        # ---Debug Configuration---
        debug = "debug" in config_dict
        verbose = "verbose" in config_dict
        if debug:
            logger.enable_debug()

        if verbose:
            logger.enable_verbose()

        # ---User Info From Args---
        if "u" in config_dict:
            username, password = config_dict["u"]
        else:
            username = input("Kullanıcı adı (@itu.edu.tr olmadan): ")
            password = getpass("Şifre: ")
        user = User(username, password)

        # ---Core Configuration---
        core_count = 2
        if "core" in config_dict:
            try:
                core_count = int(config_dict["core"][0])
            except:
                logger.warning(f"Girilen çekirdek sayısı ( {config_dict['core'][0]} ) geçerli bir sayı değil.")

        # ---Directory Configguration---
        if "d" in config_dict:
            if exists(config_dict["d"][0]):
                download_directory = config_dict["d"][0]
            else:
                logger.warning("-d ile komut satırında verilen klasör bulunamadı.")
                download_directory = filedialog.askdirectory()
        else:
            download_directory = filedialog.askdirectory()

        if not download_directory:
            logger.fail("Bir klasör seçmeniz gerekiyor.")
            exit()

        # ---First Run Detection---
        first_run = not exists(join(download_directory, DATABASE_FILE_NAME))

        if first_run:
            merge = messagebox.askyesno(
                "Klasörleri Birleştir",
                "Sınıf dosyaları ve Ders dosyaları klasörlerini birleştir?",
                icon="question",
            )
        else:
            # TEMPORARY SOLUTION!!!
            merge = False  # get "merge" from db

        # Save the changes
        cls.set_initial_attr(
            debug, user, download_directory, merge, first_run, core_count, verbose
        )
