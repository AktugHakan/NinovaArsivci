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
except ModuleNotFoundError:
    print(
        "HATA! src klasörü bulunamadı veya yeri değiştirilmiş. Programı yeniden indirin."
    )
    exit()

class Config:
    debug: bool
    user: User
    base_path: str
    session: Session
    merge: bool
    first_run: bool
    core_count: int

    @classmethod
    def set_initial_attr(cls, debug: bool, user: User, base_path: str, merge: bool, first_run: bool, core_count: int):
        cls.debug = debug
        cls.user = user
        cls.base_path = base_path
        cls.merge = merge
        cls.first_run = first_run
        cls.core_count = core_count
        from src import logger

    @classmethod
    def set_session(cls, session: Session):
        cls.session = session

    @classmethod
    def get_session_copy(cls):
        return copy.deepcopy(cls.session)
        
    @classmethod
    def init_config(cls):
        # Config from command line args
        config_dict = get_args(d=0, u=2, core=1)
        debug = "d" in config_dict
        if debug:
            logger.set_debug(True)
        else:
            logger.set_debug(False)

        if "u" in config_dict:
            username, password = config_dict["u"]
        else:
            username = input("Kullanıcı adı (@itu.edu.tr olmadan): ")
            password = getpass("Şifre: ")
        user = User(username, password)

        core_count = 2
        if "core" in config_dict:
            try:
                core_count = int(config_dict["core"])
            except:
                logger.warning("Girilen çekirdek (core) sayısı geçerli bir sayı değil.")

        download_directory = filedialog.askdirectory()
        if not download_directory:
            logger.fail("Bir klasör seçmeniz gerekiyor.")
            exit()

        first_run = not exists(join(download_directory, "files.db"))
        if first_run:
            merge = messagebox.askyesno(
                "Klasörleri Birleştir",
                "Sınıf dosyaları ve Ders dosyaları klasörlerini birleştir?",
                icon="question",
            )
        else:
            pass # get merge from db

        cls.set_initial_attr(debug, user, download_directory, merge, first_run, core_count)

