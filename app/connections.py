import sqlite3


class SQLiteConnection:

    def __init__(self, path):
        self.connection = sqlite3.connect(path, check_same_thread=False)
        self.connection.row_factory = self.dict_factory
        self.cursor = self.connection.cursor()

    @staticmethod
    def dict_factory(cursor, row):
        d = dict()
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def query_db_one(self, query):
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows[0] if rows else dict()

    def query_db(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def write_db(self, query):
        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.lastrowid

        
