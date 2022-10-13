from src import logger
from src.NinovaUrl import URL
from time import perf_counter
try:
    from bs4 import BeautifulSoup
    import requests
except ModuleNotFoundError:
    logger.fail("Gerekli kütüphaneler eksik. Yüklemek için 'pip install -r requirements.txt' komutunu çalıştırın.")
    exit()

def check_connection() -> bool:
    CHECK_CONNECTIVITY_URL = "http://www.example.com/"
    try:
        requests.get(CHECK_CONNECTIVITY_URL)
        return True
    except:
        return False


def login(SECURE_INFO: tuple[str, str]) -> requests.Session:
    global URL
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
        logger.warning("Ninova sunucusuna bağlanılamadı.")
        if check_connection():
            logger.fail("Internet var ancak Ninova'ya bağlanılamıyor.")
            exit()
        else:
            logger.fail("Internete erişim yok. Bağlantınızı kontrol edin.")
            exit()

    page = BeautifulSoup(page.content, "lxml")

    post_data = dict()
    for field in page.find_all("input"):
        post_data[field.get("name")] = field.get("value")
    post_data["ctl00$ContentPlaceHolder1$tbUserName"] = SECURE_INFO[0]
    post_data["ctl00$ContentPlaceHolder1$tbPassword"] = SECURE_INFO[1]

    start = perf_counter()
    page = session.post(
        "https://girisv3.itu.edu.tr" + page.form.get("action")[1:], data=post_data
    )
    end = perf_counter()
    elapsed = end-start
    logger.debug(f"Giriş yapma işlemi {elapsed} saniye sürdü")

    page = BeautifulSoup(page.content, "lxml")
    if page.find(id="ctl00_Header1_tdLogout") is None:
        logger.fail("Giriş yapılamadı!")
        exit()
    return session
