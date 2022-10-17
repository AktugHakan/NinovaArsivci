from __future__ import annotations
from concurrent.futures import thread
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from requests import Session
    from src.kampus import Course

from src.kampus import Course
from time import perf_counter
from src.NinovaUrl import URL
from os import mkdir
from os.path import join
from src import logger
from bs4 import BeautifulSoup, element
from threading import Thread

MIN_FILE_SIZE_TO_LAUNCH_NEW_THREAD = 5  # in mb

SINIF_DOSYALARI_URL_EXTENSION = "/SinifDosyalari"
DERS_DOSYALARI_URL_EXTENSION = "/DersDosyalari"

thread_list: list[Thread] = []
# Currently does not traverse folders
def download_all_in_course(
    session: Session, course: Course, base_download_directory: str, merge: bool
) -> None:
    global URL

    subdir_name = join(base_download_directory, course.code)

    try:
        mkdir(subdir_name)
        logger.debug(f"{subdir_name} klasörü oluşturuldu.")
    except FileExistsError:
        logger.debug(
            f"{subdir_name} klasörü oluşturulmadı. Zaten böyle bir klasör var."
        )

    if merge:
        raw_html = session.get(
            URL + course.link + SINIF_DOSYALARI_URL_EXTENSION
        ).content.decode("utf-8")

        _download_or_traverse(session, raw_html, subdir_name)

        raw_html = session.get(
            URL + course.link + DERS_DOSYALARI_URL_EXTENSION
        ).content.decode("utf-8")

        _download_or_traverse(session, raw_html, subdir_name)
    else:
        raw_html = session.get(
            URL + course.link + SINIF_DOSYALARI_URL_EXTENSION
        ).content.decode("utf-8")

        try:
            klasor = join(subdir_name, "Sınıf Dosyaları")
            mkdir(klasor)
        except FileExistsError:
            pass

        _download_or_traverse(session, raw_html, klasor)

        raw_html = session.get(
            URL + course.link + DERS_DOSYALARI_URL_EXTENSION
        ).content.decode("utf-8")

        try:
            klasor = join(subdir_name, "Ders Dosyaları")
            mkdir(klasor)
        except FileExistsError:
            pass

        _download_or_traverse(session, raw_html, klasor)

        for thread in thread_list:
            thread.join()


def get_mb_file_size_from_string(raw_file_size: str) -> float:
    size_info = raw_file_size.strip().split(" ")
    size_as_float = float(size_info[0])
    if size_info[1] == "KB":
        size_as_float / 1024
    return size_as_float


def _download_or_traverse(
    session: Session, raw_html: str, destionation_folder: str
) -> None:
    try:
        rows = BeautifulSoup(raw_html, "lxml")
        rows = rows.select_one(".dosyaSistemi table.data").find_all("tr")
    except:
        return  # if the 'file' is a link to another page
    rows.pop(0)  # first row is the header of the table

    row: element.Tag
    for row in rows:
        info = parse_file_info(row)
        if info:
            file_link, file_size, isFolder, file_name = info
            if isFolder:
                traverse_folder(
                    session, URL + file_link, destionation_folder, file_name
                )
            elif file_size > MIN_FILE_SIZE_TO_LAUNCH_NEW_THREAD:  # mb
                large_file_thread = Thread(
                    target=download_file,
                    args=(session, URL + file_link, destionation_folder),
                )
                large_file_thread.start()
                thread_list.append(large_file_thread)
            else:
                download_file(session, URL + file_link, destionation_folder)


def parse_file_info(row: element.Tag):

    try:
        file_info = row.find_all("td")  # ("td").find("a")
        file_a_tag = file_info[0].find("a")
        file_name = file_a_tag.text
        file_size = get_mb_file_size_from_string(file_info[1].text)
        isFolder = file_info[0].find("img")["src"].endswith("/folder.png")
        file_link = file_a_tag["href"]
    except:
        return None

    return file_link, file_size, isFolder, file_name


def traverse_folder(session, folder_url, current_folder, new_folder_name):
    resp = session.get(folder_url)
    subdir_name = join(current_folder, new_folder_name)
    try:
        mkdir(subdir_name)
        logger.debug(f"{new_folder_name} klasörü oluşturuldu")
    except FileExistsError:
        logger.debug(f"{subdir_name} klasörü oluşturulmadı, bu klasör zaten var.")

    folder_thread = Thread(
        target=_download_or_traverse,
        args=(session, resp.content.decode("utf-8"), subdir_name),
    )
    folder_thread.start()
    thread_list.append(folder_thread)


def download_file(session, file_url, destination_folder):
    start = perf_counter()
    resp = session.get(file_url)
    end = perf_counter()
    file_name_offset = resp.headers["content-disposition"].index("filename=") + 9
    file_name = resp.headers["content-disposition"][file_name_offset:]
    logger.debug(f"{file_name:<15} dosyası {end-start} saniyede indirildi.")
    with open(destination_folder + "/" + file_name, "wb") as bin:
        bin.write(resp.content)
