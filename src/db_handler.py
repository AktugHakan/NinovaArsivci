from collections import namedtuple
import sqlite3
from os.path import join, exists
from enum import Enum
from zlib import crc32
from queue import Queue

from src import logger
from src import globals

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

FileRecord = namedtuple("FileRecord", "id, path")

class DB:
    connection: sqlite3.Connection
    to_add = Queue()
    db_path: str

    @classmethod
    def init(cls):
        """
        Connects to DB and checks and creates the table structure
        """
        cls.db_path = join(globals.BASE_PATH, DATABASE_FILE_NAME)
        cls.connect()
        cursor = cls.connection.cursor()
        if globals.FIRST_RUN:
            cursor.execute(TABLE_CREATION_QUERY)
            logger.verbose("Veri tabanı ilk çalıştırma için hazırlandı.")
        else:
            cursor.execute(TABLE_CHECK_QUERY)
            if cursor.fetchone()[0] != "files":
                logger.fail(
                    f"Veri tabanı bozuk. '{DATABASE_FILE_NAME}' dosyasını silip tekrar başlatın. Silme işlemi sonrasında tüm dosyalar yeniden indirilir."
                )

        cursor.close()

    @classmethod
    def connect(cls):
        """
        Connects to DB using db_path class attribute
        Sets connection object of the class, does not return anything
        """
        try:
            cls.connection = sqlite3.connect(cls.db_path, check_same_thread=False)
            logger.debug("Veri tabanına bağlandı.")
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
                    "Eş zamanlı erişimden dolayı, race condition oluşturdu. Veri tabanından gelen bilgi, bu dosyaya ait değil. Geliştiriciye bildirin."
                )

            if deleted:
                return FILE_STATUS.DELETED
            else:
                return FILE_STATUS.EXISTS
        else:
            return FILE_STATUS.NEW

    # Should be called after the download
    @classmethod
    def add_file(cls, id: int, path: str):
        cls.to_add.put(FileRecord(id, path))

    @classmethod
    def apply_changes_and_close(cls):
        cls.connection.commit()
        cls.connection.close()

    @classmethod
    def get_new_cursor(cls):
        return cls.connection.cursor()

    @classmethod
    @logger.speed_measure("Veri tabanına yazma", False, False)
    def write_records(cls):
        cursor = cls.get_new_cursor()
        while not cls.to_add.empty():
            record = cls.to_add.get()
            if exists(record.path):
                with open(record.path, "rb") as file:
                    hash = crc32(file.read())
                    try:
                        cursor.execute(FILE_INSERTION_QUERY, (record.id, record.path, hash))
                    except Exception as e:
                        logger.fail(str(e) + "\n The file_path is " + record.path)
            else:
                logger.warning(f"Veritabanına yazılacak {record.path} dosyası bulunamadı. Veri tabanına yazılmayacak")

        cls.apply_changes_and_close()
        
        
