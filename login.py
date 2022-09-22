import requests
from bs4 import BeautifulSoup

def login():
    # Text coloring
    FAIL = '\033[91m'
    ENDC = '\033[0m'

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
        print(f"{FAIL}Kullanıcı adı ve şifre bulunamadı{ENDC}\nLütfen aynı klasör içine {SECURE_INFO_FILE} dosyasını oluşturun ve \nilk satıra kullanıcı adı ikinci satıra şifrenizi yazın.")
    except PermissionError:
        print(f"{FAIL}Programın dosya sistemine erişimi yok!{ENDC}")

    # Requesting and parsing the page
    session = requests.Session()
    page = session.get(URL, headers=HEADERS)
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