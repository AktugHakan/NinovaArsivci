from bs4 import BeautifulSoup
from src.NinovaUrl import URL
from tkinter import filedialog as fd

SINIF_DOSYALARI_URL_EXTENSION = "/SinifDosyalari"

# Currently does not traverse folders
def download_all(session, course):
    global URL
    download_directory = fd.askdirectory()
    raw_html = session.get(URL + course.link + SINIF_DOSYALARI_URL_EXTENSION).content.decode("utf-8")
    _download_or_traverse(session, raw_html, download_directory)
    

def _download_or_traverse(session, raw_html, destionation_folder):
    files = BeautifulSoup(raw_html, "lxml")
    files = files.select_one(".dosyaSistemi table.data").find_all("tr")
    files.pop(0) # first row is the header of the table

    for file in files:
        file_link = file.find("td").find("a")["href"]
        resp = session.get(URL + file_link)
        if "text/html" in resp.headers["content-type"]:
            _download_or_traverse(session, resp.content.decode("utf-8"), destionation_folder)
        else:
            file_name_offset = resp.headers["content-disposition"].index("filename=") + 9
            file_name = resp.headers["content-disposition"][file_name_offset:]
            with open(destionation_folder + "/" + file_name, "wb") as bin:
                bin.write(resp.content)



