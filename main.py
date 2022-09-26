# getpass does not show anything while password is entered but pwinput shows ***
# pwinput looks better but it is not in standard library

# ---IMPORTS---
try:
    from pwinput import pwinput as getpass
except:
    from getpass import getpass

from sys import argv
from src.login import login

# ---CONSTANTS---
URL = "https://ninova.itu.edu.tr/Kampus1"


# ---MAIN---

if(len(argv) == 3):
    username = argv[1]
    password = argv[2]
else:
    username = input("Kullanıcı adı (@itu.edu.tr olmadan): ")
    password = getpass("Şifreniz: ")

user = (username, password)

session = login(URL, user)

page = session.get(URL)
print(page)
