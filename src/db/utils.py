import sqlite3
from contextlib import contextmanager


@contextmanager
def sql_execute(db_name: str):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    yield cursor

    conn.commit()
    conn.close()
