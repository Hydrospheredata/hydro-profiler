import sqlite3


class SqliteContextManager:
    def __init__(self):
        pass

    def __enter__(self):
        self.con = sqlite3.connect(
            "profiler/resources/db/sqlite/profiler.db", check_same_thread=False
        )
        cur = self.con.cursor()

        return cur

    def __exit__(self, type, value, traceback):
        self.con.commit()
        self.con.close()
