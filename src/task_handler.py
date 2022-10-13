from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from requests import Session
    from src.kampus import Course

from src.downloader import download_all_in_course
from multiprocessing import Process


def start_tasks(
    session: Session, courses: list[Course], download_directory: str, merge: bool
) -> None:
    proc_list: list[Process] = []
    for course in courses:
        proc = Process(
            target=download_all_in_course,
            args=(session, course, download_directory, merge),
        )
        proc.start()
        proc_list.append(proc)

    for proc in proc_list:
        proc.join()
