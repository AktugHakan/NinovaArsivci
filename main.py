# getpass does not show anything while password is entered but pwinput shows ***
# pwinput looks better but it is not in standard library

# ---IMPORTS---
try:
    from pwinput import pwinput as getpass
except:
    from getpass import getpass

from sys import argv
from src.login import login
from src.kampus import get_course_list
from src.downloader import download_all

# ---MAIN---

if(len(argv) == 3):
    username = argv[1]
    password = argv[2]
else:
    username = input("Kullanıcı adı (@itu.edu.tr olmadan): ")
    password = getpass("Şifreniz: ")
user = (username, password)

session = login(user)
courses = get_course_list(session)

download_all(session, courses[3])