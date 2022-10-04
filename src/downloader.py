from bs4 import BeautifulSoup
from src.NinovaUrl import URL
from os import mkdir
from os.path import join
from src import logger

SINIF_DOSYALARI_URL_EXTENSION = "/SinifDosyalari"

# Currently does not traverse folders
def download_all_in_course(session, course, base_download_directory):
    global URL

    if not base_download_directory:
        logger.fail("Bir klasör seçmeniz gerekiyor.")
        exit()

    subdir_name = join(base_download_directory, course.code)
    try:
        mkdir(subdir_name)
    except FileExistsError:
        logger.debug(
            f"{subdir_name} klasörü oluşturulmadı. Zaten böyle bir klasör var."
        )
    raw_html = session.get(
        URL + course.link + SINIF_DOSYALARI_URL_EXTENSION
    ).content.decode("utf-8")
    _download_or_traverse(session, raw_html, subdir_name)


def _download_or_traverse(session, raw_html, destionation_folder):
    rows = BeautifulSoup(raw_html, "lxml")
    rows = rows.select_one(".dosyaSistemi table.data").find_all("tr")
    rows.pop(0)  # first row is the header of the table

    for row in rows:
        file_a_tag = row.find("td").find("a")
        file_link = file_a_tag["href"]
        element_name = file_a_tag.text
        resp = session.get(URL + file_link)
        if "text/html" in resp.headers["content-type"]:
            subdir_name = join(destionation_folder, element_name)
            try:
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
