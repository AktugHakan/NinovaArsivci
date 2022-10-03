from bs4 import BeautifulSoup
from src.NinovaUrl import URL
from tkinter import filedialog as fd

SINIF_DOSYALARI_URL_EXTENSION = "/SinifDosyalari"

# Currently does not traverse folders
def download_all(session, course):
    global URL
    download_directory = fd.askdirectory()
    files = BeautifulSoup(session.get(URL + course.link + SINIF_DOSYALARI_URL_EXTENSION).content.decode("utf-8"), "lxml")
    files = files.select_one(".dosyaSistemi table.data").find_all("tr")
    files.pop(0)
    for file in files:
        file_link = file.find("td").find("a")["href"]
        resp = session.get(URL + file_link)
        file_name_offset = resp.headers["content-disposition"].index("filename=") + 9
        file_name = resp.headers["content-disposition"][file_name_offset:]
        with open(download_directory + "/" + file_name, "wb") as bin:
            bin.write(resp.content)



