import sqlite3
from multiprocessing import Queue
from os.path import join

from src.configuration import Config
from src import logger

DATABASE_FILE_NAME = "ninova_arsivci.db"
TABLE_CREATION_QUERY = "CREATE TABLE files (id INTEGER PRIMARY KEY, path TEXT UNIQUE, hash INT, isDeleted INT DEFAULT 0);"
TABLE_CHECK_QUERY = (
    "SELECT name FROM sqlite_master WHERE type='table' AND name='files';"
)


class DB:
    connection: sqlite3.Connection
    cursor: sqlite3.Cursor
    to_add: Queue = Queue()

    @classmethod
    def init(cls, base_directory: str):
        db_path = join(base_directory, DATABASE_FILE_NAME)
        try:
            cls.connection = sqlite3.connect(db_path)
            cls.cursor = cls.connection.cursor()
            logger.debug("Veri tabanına bağlanıldı.")
        except:
            logger.fail("Veri tabanına bağlanılamadı.")

        if Config.first_run:
            cls.cursor.execute(TABLE_CREATION_QUERY)
            logger.info("Veri tabanı ilk çalıştırma için hazırlandı.")
        else:
            cls.cursor.execute(TABLE_CHECK_QUERY)
            if cls.cursor.getCount() < 1:
                logger.fail(
                    "Veri tabanı bozulmuş. 'ninova_arsivci.db' dosyasını silip tekrar başlatın. Silme işlemi sonrasında tüm dosyalar yeniden indirilir."
                )

