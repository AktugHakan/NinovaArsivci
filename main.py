# getpass does not show anything while password is entered but pwinput shows ***
# pwinput looks better but it is not in standard library

# ---IMPORTS---
try:
    from pwinput import pwinput as getpass
except:
    from getpass import getpass

from src import logger
from sys import argv
from time import perf_counter
from src.login import login
from src.kampus import get_course_list
from src.downloader import download_all_in_course
from tkinter import filedialog, messagebox

# ---MAIN---
start = perf_counter()


if len(argv) == 3:
    username = argv[1]
    password = argv[2]
else:
    username = input("Kullanıcı adı (@itu.edu.tr olmadan): ")
    password = getpass("Şifreniz: ")
user = (username, password)

session = login(user)
courses = get_course_list(session)

start_user_delay = perf_counter()
download_directory = filedialog.askdirectory()

merge = messagebox.askyesno(
    "Klasörleri Birleştir veya Ayır",
    "Sınıf dosyaları ve Ders dosyaları klasörlerini birleştir?",
    icon="question",
)
stop_user_delay = perf_counter()

for course in courses:
    download_all_in_course(session, course, download_directory, merge)


end = perf_counter()
logger.verbose(
    f"İş {(end-start) - (stop_user_delay-start_user_delay)} saniyede tamamlandı."
)
