# getpass does not show anything while password is entered but pwinput shows ***
# pwinput looks better but it is not in standard library

# ---IMPORTS---
try:
    from src.configuration import Config

    from src import logger
    from src.login import login
    from src.kampus import get_course_list
    from src.task_handler import start_tasks
except ModuleNotFoundError:
    print(
        "HATA! src klasörü bulunamadı veya yeri değiştirilmiş. Programı yeniden indirin."
    )
    exit()

# ---MAIN---
if __name__ == "__main__":
    # Get username from command line, else prompt
    Config.init_config()

    session = login(Config.user)
    Config.set_session(session)

    courses = get_course_list()

    start_tasks(courses)





