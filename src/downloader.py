from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.kampus import Course

from os import mkdir
from os.path import join, exists
from src import logger
from bs4 import BeautifulSoup, element
from threading import Thread
from zlib import crc32

from src import globals
from src.login import URL
from src.db_handler import DB, FILE_STATUS

MIN_FILE_SIZE_TO_LAUNCH_NEW_THREAD = 5  # in mb

SINIF_DOSYALARI_URL_EXTENSION = "/SinifDosyalari"
DERS_DOSYALARI_URL_EXTENSION = "/DersDosyalari"

thread_list: list[Thread] = []


def download_all_in_course(course: Course) -> None:
    global URL

    subdir_name = join(globals.BASE_PATH, course.code)

    session = globals.session_copy()

    try:
        mkdir(subdir_name)
    except FileExistsError:
        pass

    raw_html = session.get(
        URL + course.link + SINIF_DOSYALARI_URL_EXTENSION
    ).content.decode("utf-8")

    try:
        klasor = join(subdir_name, "Sınıf Dosyaları")
        mkdir(klasor)
    except FileExistsError:
        pass

    _download_or_traverse(raw_html, klasor)

    raw_html = session.get(
        URL + course.link + DERS_DOSYALARI_URL_EXTENSION
    ).content.decode("utf-8")

    try:
        klasor = join(subdir_name, "Ders Dosyaları")
        mkdir(klasor)
    except FileExistsError:
        pass

    _download_or_traverse(raw_html, klasor)

    for thread in thread_list:
        thread.join()


def _get_mb_file_size_from_string(raw_file_size: str) -> float:
    size_info = raw_file_size.strip().split(" ")
    size_as_float = float(size_info[0])
    if size_info[1] == "KB":
        size_as_float / 1024
    return size_as_float


def _download_or_traverse(raw_html: str, destionation_folder: str) -> None:
    session = globals.session_copy()
    try:
        rows = BeautifulSoup(raw_html, "lxml")
        rows = rows.select_one(".dosyaSistemi table.data").find_all("tr")
    except:
        return  # if the 'file' is a link to another page
    rows.pop(0)  # first row is the header of the table

    row: element.Tag
    for row in rows:
        info = _parse_file_info(row)
        if info:
            file_link, file_size, isFolder, file_name = info
            if isFolder:
                _traverse_folder(
                    URL + file_link, destionation_folder, file_name
                )
            elif file_size > MIN_FILE_SIZE_TO_LAUNCH_NEW_THREAD:  # mb
                large_file_thread = Thread(
                    target=_download_file,
                    args=(
                        URL + file_link,
                        destionation_folder,
                        DB.get_new_cursor(),
                    ),
                )
                large_file_thread.start()
                thread_list.append(large_file_thread)
            else:
                _download_file(
                    URL + file_link, destionation_folder, DB.get_new_cursor()
                )


def _parse_file_info(row: element.Tag):
    try:
        file_info = row.find_all("td")  # ("td").find("a")
        file_a_tag = file_info[0].find("a")
        file_name = file_a_tag.text
        file_size = _get_mb_file_size_from_string(file_info[1].text)
        isFolder = file_info[0].find("img")["src"].endswith("/folder.png")
        file_link = file_a_tag["href"]
    except:
        return None

    return file_link, file_size, isFolder, file_name


def _traverse_folder(folder_url, current_folder, new_folder_name):
    session = globals.session_copy()
    resp = session.get(folder_url)
    subdir_name = join(current_folder, new_folder_name)
    try:
        mkdir(subdir_name)
    except FileExistsError:
        pass

    folder_thread = Thread(
        target=_download_or_traverse,
        args=(resp.content.decode("utf-8"), subdir_name),
    )
    folder_thread.start()
    thread_list.append(folder_thread)


def _download_file(file_url: str, destination_folder: str, cursor):
    session = globals.session_copy()
    file_status = DB.check_file_status(int(file_url[file_url.find("?g") + 2 :]), cursor)
    match file_status:
        case FILE_STATUS.NEW:
            file_name, file_binary = _download_from_server(session, file_url)
            file_full_name = join(destination_folder, file_name)
            while exists(file_full_name):
                ex_file = open(file_full_name, "rb")
                if crc32(file_binary) != crc32(ex_file.read()):
                    extension_dot_index = file_full_name.find(".")
                    file_full_name = (
                        file_full_name[:extension_dot_index]
                        + "_new"
                        + file_full_name[extension_dot_index:]
                    )
                else:
                    if not globals.FIRST_RUN:
                        logger.warning(
                            "Veri tabanına manuel müdahele tespit edildi. Eğer müdahele edilmediyse geliştiriciye bildirin!"
                        )
                    break

            with open(file_full_name, "wb") as bin:
                bin.write(file_binary)

            DB.add_file(int(file_url[file_url.find("?g") + 2 :]), file_full_name)


@logger.speed_measure("indirme işlemi", False, True)
def _download_from_server(session, file_url: str):
    resp = session.get(file_url)
    file_name_offset = resp.headers["content-disposition"].index("filename=") + 9
    file_name = resp.headers["content-disposition"][file_name_offset:]
    return file_name, resp.content
