# getpass does not show anything while password is entered but pwinput shows ***
# pwinput looks better but it is not in standard library

# ---IMPORTS---
try:
    from src import logger
    from src.login import login
    from src.kampus import get_course_list
    from src.task_handler import start_tasks
    from src.db_handler import DB
    from src import globals
except ModuleNotFoundError:
    print(
        "HATA! Kütphaneler yüklenemedi. 'src' klasörü silinmiş veya yeri değişmiş olabilir."
    )
    exit()

# ---MAIN---
@logger.speed_measure("Program", False)
def main():
    DB.init()

    courses = get_course_list()
    start_tasks(courses)

    DB.write_records()
    
    input("Press a key to close the terminal.") # To prevent the terminal from closing automatically when you open the program with a .bat file


# ---Program driving code---
if __name__ == "__main__":
    globals.init_globals()
    main()
