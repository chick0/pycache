from threading import Thread

from . import STORAGE
from .log import clean


def _work(memory: int):
    while memory > STORAGE.__limit__:
        key = None
        for q in STORAGE:
            key = q
            break

        clean(key=key, memory=f"{memory} > {STORAGE.__limit__}")
        memory -= STORAGE.get(key).__sizeof__()
        STORAGE.pop(key)


def clean_up(memory: int):
    Thread(target=_work, args=(memory,)).start()
