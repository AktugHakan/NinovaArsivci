from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from requests import Session
    from src.kampus import Course

import copy
from src.downloader import download_all_in_course
from threading import Thread
from multiprocessing import Process


def start_tasks(
    session: Session, courses: list[Course], download_directory: str, merge: bool
) -> None:
    core1 = Process(
        target=thread_launcher,
        args=(session, courses[: (len(courses) // 2)], download_directory, merge),
    )
    core2 = Process(
        target=thread_launcher,
        args=(session, courses[(len(courses) // 2) + 1 :], download_directory, merge),
    )
    core1.start()
    core2.start()
    core1.join()
    core2.join()


def thread_launcher(
    session: Session, courses: list[Course], download_directory: str, merge: bool
) -> None:
    proc_list: list[Thread] = []
    for course in courses:
        session_copy = copy.deepcopy(session)
        proc = Thread(
            target=download_all_in_course,
            args=(session_copy, course, download_directory, merge),
        )
        proc.start()
        proc_list.append(proc)

    for proc in proc_list:
        proc.join()
