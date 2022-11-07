import sqlite3
from multiprocessing import Queue
from os.path import join, exists
from enum import Enum
from zlib import crc32

from src import logger

DATABASE_FILE_NAME = "ninova_arsivci.db"
TABLE_CREATION_QUERY = "CREATE TABLE files (id INTEGER PRIMARY KEY, path TEXT UNIQUE, hash INT, isDeleted INT DEFAULT 0);"
TABLE_CHECK_QUERY = (
    "SELECT name FROM sqlite_master WHERE type='table' AND name='files';"
)
SELECT_FILE_BY_ID_QUERY = "SELECT isDeleted, id FROM files WHERE id = ?"
FILE_INSERTION_QUERY = "INSERT INTO files (id, path, hash) VALUES (?, ?, ?)"


class FILE_STATUS(Enum):
    NEW = 0
    DELETED = 1
    EXISTS = 2


class DB:
    connection: sqlite3.Connection
    to_add: Queue = Queue()
    db_path: str

    @classmethod
    def init(cls, base_directory: str, first_run: bool):
        cls.db_path = join(base_directory, DATABASE_FILE_NAME)
        cls.connect(cls.db_path)
        cursor = cls.connection.cursor()
        if first_run:
            cursor.execute(TABLE_CREATION_QUERY)
            logger.verbose("Veri tabanı ilk çalıştırma için hazırlandı.")
        else:
            cursor.execute(TABLE_CHECK_QUERY)
            if cursor.fetchone()[0] != "files":
                logger.fail(
                    "Veri tabanı bozulmuş. 'ninova_arsivci.db' dosyasını silip tekrar başlatın. Silme işlemi sonrasında tüm dosyalar yeniden indirilir."
                )

        cursor.close()

    @classmethod
    def connect(cls, db_path):
        try:
            cls.connection = sqlite3.connect(db_path, check_same_thread=False)

            logger.debug("Veri tabanına bağlanıldı.")
        except:
            logger.fail("Veri tabanına bağlanılamadı.")

    # takes file_id, finds and returns the status from database
    # file_id is the end of the file url (after question mark - question mark and 'g' is not included)
    @classmethod
    def check_file_status(cls, file_id: int, cursor: sqlite3.Cursor):
        cursor.execute(SELECT_FILE_BY_ID_QUERY, (file_id,))
        file = cursor.fetchone()
        if file:
            deleted, id = file
            if file_id != id:
                logger.fail(
                    "Eş zamanlı erişim, race condition oluşturdu. Veri tabanından gelen bilgi, bu dosyaya ait değil."
                )

            if deleted:
                return FILE_STATUS.DELETED
            else:
                return FILE_STATUS.EXISTS
        else:
            return FILE_STATUS.NEW

    # Should be called after the download
    @classmethod
    def add_file(cls, id: int, path: str, cursor: sqlite3.Cursor):
        if exists(path):
            with open(path, "rb") as file:
                hash = crc32(file.read())
                try:
                    cursor.execute(FILE_INSERTION_QUERY, (id, path, hash))
                except Exception as e:
                    logger.fail(str(e) + "\n The file_path is " + path)
        else:
            logger.fail("Given file to add to DB, cannot found in disk.")

    @classmethod
    def apply_changes_and_close(cls):
        cls.connection.commit()
        cls.connection.close()

    @classmethod
    def get_new_cursor(cls):
        return cls.connection.cursor()