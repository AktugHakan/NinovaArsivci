from cmath import log
import requests, logging
from bs4 import BeautifulSoup


# Text coloring
FAIL = '\033[91m'
ENDC = '\033[0m'
WARNING = '\033[93m'

def check_connection():
    CHECK_CONNECTIVITY_URL = "http://www.example.com/"
    try:
        requests.get(CHECK_CONNECTIVITY_URL)
        return True
    except:
        return False

def login():
    # Meta-data
    URL = "https://ninova.itu.edu.tr/Kampus1"
    HEADERS = {
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding" : "gzip, deflate, br",
        "Connection" : "keep-alive",
        "DNT" : "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0"
    }
    USER_NAME = None
    PASSWORD = None
    SECURE_INFO_FILE = "secure.txt"

    # Getting username and password from file
    try:
        with open(SECURE_INFO_FILE, "r") as f:
            USER_NAME = f.readline().strip(" \n")
            PASSWORD = f.readline().strip(" \n")
    except FileNotFoundError:
        raise FileNotFoundError(f"{FAIL}Kullanıcı adı ve şifre bulunamadı{ENDC}\nLütfen aynı klasör içine {SECURE_INFO_FILE} dosyasını oluşturun ve \nilk satıra kullanıcı adı ikinci satıra şifrenizi yazın.")
    except PermissionError:
        raise PermissionError(f"{FAIL}Programın dosya sistemine erişimi yok!{ENDC}")

    # Requesting and parsing the page
    session = requests.Session()
    try:
        page = session.get(URL, headers=HEADERS)
    except:
        logging.warning(f"{WARNING}{URL}'a bağlanılamadı. İnternet bağlantı kontrol ediliyor.{ENDC}")
        if check_connection():
            raise ConnectionError(f"{FAIL}İnternet var ancak Ninova'ya bağlanılamıyor.{ENDC}")
        else:
            raise ConnectionError(f"{FAIL}Internete erişim yok. Bağlantınızı kontrol edin.{ENDC}")


    page = BeautifulSoup(page.content, "lxml")

    post_data = dict()
    for field in page.find_all("input"):
        post_data[field.get("name")] = field.get("value")
    post_data["ctl00$ContentPlaceHolder1$tbUserName"] = USER_NAME
    post_data["ctl00$ContentPlaceHolder1$tbPassword"] = PASSWORD
    page = session.post("https://girisv3.itu.edu.tr" + page.form.get("action")[1:], data=post_data)
    page = BeautifulSoup(page.content, "lxml")
    if page.find(id="ctl00_Header1_tdLogout") is None:
        raise Exception("Giriş yapılamadı!")
    return page, session