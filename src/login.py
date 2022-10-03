from src import text_coloring
import requests, logging
from bs4 import BeautifulSoup
from src.NinovaUrl import URL


def check_connection():
    CHECK_CONNECTIVITY_URL = "http://www.example.com/"
    try:
        requests.get(CHECK_CONNECTIVITY_URL)
        return True
    except:
        return False


def login(SECURE_INFO):
    URL = URL + "/Kampus1"
    HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0",
    }

    # Requesting and parsing the page
    session = requests.Session()
    try:
        page = session.get(URL, headers=HEADERS)
    except:
        logging.warning(
            text_coloring.warning(
                "Ninova'ya bağlanılamadı. İnternet bağlantı kontrol ediliyor."
            )
        )
        if check_connection():
            raise ConnectionError(
                text_coloring.fail("Internet var ancak Ninova'ya bağlanılamıyor.")
            )
        else:
            raise ConnectionError(
                text_coloring.fail("Internete erişim yok. Bağlantınızı kontrol edin.")
            )

    page = BeautifulSoup(page.content, "lxml")

    post_data = dict()
    for field in page.find_all("input"):
        post_data[field.get("name")] = field.get("value")
    post_data["ctl00$ContentPlaceHolder1$tbUserName"] = SECURE_INFO[0]
    post_data["ctl00$ContentPlaceHolder1$tbPassword"] = SECURE_INFO[1]
    page = session.post(
        "https://girisv3.itu.edu.tr" + page.form.get("action")[1:], data=post_data
    )
    page = BeautifulSoup(page.content, "lxml")
    if page.find(id="ctl00_Header1_tdLogout") is None:
        raise Exception("Giriş yapılamadı!")
    return session
