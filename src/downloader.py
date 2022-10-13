from __future__ import annotations
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
from bs4 import BeautifulSoup



SINIF_DOSYALARI_URL_EXTENSION = "/SinifDosyalari"
DERS_DOSYALARI_URL_EXTENSION = "/DersDosyalari"

# Currently does not traverse folders
def download_all_in_course(session: Session, course: Course, base_download_directory: str, merge: bool) -> None:
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


def _download_or_traverse(session: Session, raw_html: str, destionation_folder: str) -> None:
    try:
        rows = BeautifulSoup(raw_html, "lxml")
        rows = rows.select_one(".dosyaSistemi table.data").find_all("tr")
    except:
        return # if the 'file' is a link to another page
    rows.pop(0)  # first row is the header of the table

    for row in rows:
        file_a_tag = row.find("td").find("a")
        try:
            file_link = file_a_tag["href"]
        except:
            return
        element_name = file_a_tag.text
        start = perf_counter()
        resp = session.get(URL + file_link)
        end = perf_counter()
        logger.debug(f"Ninova'ya yapılan {element_name[:15]:<15} isteği {end-start} saniyede yanıtlandı.")
        if "text/html" in resp.headers["content-type"]:
            subdir_name = join(destionation_folder, element_name)
            try:
                logger.debug(f"{element_name} klasörü oluşturuluyor")
                mkdir(subdir_name)
            except FileExistsError:
                logger.debug(
                    f"{subdir_name} klasörü oluşturulmadı. Zaten böyle bir klasör var."
                )
            _download_or_traverse(session, resp.content.decode("utf-8"), subdir_name)
        else:
            file_name_offset = (
                resp.headers["content-disposition"].index("filename=") + 9
            )
            file_name = resp.headers["content-disposition"][file_name_offset:]
            with open(destionation_folder + "/" + file_name, "wb") as bin:
                bin.write(resp.content)
