from collections import namedtuple
from bs4 import BeautifulSoup
from src.text_coloring import fail

Course = namedtuple("Course", "code name link")
COURSE_TITLE_OFFSET = 8

def get_course_list(session, URL):
    course_list = []

    page = BeautifulSoup(session.get(URL + "/Kampus1").content.decode("utf-8"), "lxml")

    erisim_agaci = page.select(".menuErisimAgaci>ul>li")
    for element in erisim_agaci:
        link = element.find("a")["href"]
        ders_info = BeautifulSoup(session.get(URL + link + "/SinifBilgileri").content.decode("utf-8"), "lxml")
        ders_info = ders_info.find(class_ = "formAbetGoster")
        ders_info = ders_info.select("tr")
        code = ders_info[0].select("td")[1].text.strip()
        name = ders_info[1].select("td")[2].text.strip()
        
        course_list.append(Course(code ,name, link))
    for course in course_list:
        print(course)

# https://ninova.itu.edu.tr/Sinif/2123.82531/SinifBilgileri