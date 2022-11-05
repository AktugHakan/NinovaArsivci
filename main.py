# getpass does not show anything while password is entered but pwinput shows ***
# pwinput looks better but it is not in standard library

# ---IMPORTS---
try:
    from src.configuration import Config
    from src import logger
    from src.login import login
    from src.kampus import get_course_list
    from src.task_handler import start_tasks
    from src.argv_handler import get_args
    from src.db_handler import DB
except ModuleNotFoundError:
    print(
        "HATA! Kütphaneler yüklenemedi. 'src' klasörü silinmiş veya yeri değişmiş olabilir."
    )
    exit()

# ---MAIN---
@logger.speed_measure("Program", False)
def main():
    session = login(Config.user)
    Config.set_session(session)

    courses = get_course_list()
    start_tasks(courses)


# ---Program driving code---
if __name__ == "__main__":
    # Config.init should be called before main, since main uses user info in the config
    Config.init()
    DB.init()
    main()
