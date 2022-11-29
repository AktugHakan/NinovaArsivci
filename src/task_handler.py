from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.kampus import Course

from threading import Thread

from src.downloader import download_all_in_course



def start_tasks(courses: list[Course]) -> None:
    proc_list: list[Thread] = []
    for course in courses:
        proc = Thread(
            target=download_all_in_course,
            args=(course,)
        )
        proc.start()
        proc_list.append(proc)

    for proc in proc_list:
        proc.join()