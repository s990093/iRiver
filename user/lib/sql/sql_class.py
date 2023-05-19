import MySQLdb
import json
import difflib


class SQL:
    def __init__(self, config):
        self.config = config
        self.table_name = None
        self.connect()

    def connect(self):
        self.db = MySQLdb.connect(**self.config)
        self.cursor = self.db.cursor()

    def create_table(self, table_name):
        print("-"*30)
        print(f"created table {table_name}")

    def commit(self, method: str, **kwargs):
        if method == "insert":
            self.insert(**kwargs)
        elif method == "update":
            self.updata(**kwargs)
        else:
            print("-"*30)
            print(f"the method {method} is not supported")
            return False

    def insert(self, sql: str, values):
        print(values)
        self.show(sql=sql, kwargs=values)
        self.execute(sql=sql, values=values)

    def updata(self, sql: str, values):
        self.show(sql=sql, kwargs=values)
        self.execute(sql=sql, values=values)

    def select(self, sql: str, values):
        self.show(sql=sql, kwargs=values)
        self.execute(sql=sql, values=values)

    def execute(self, sql, values, isALL=False):
        self.cursor.execute(sql, values)
        self.db.commit()
        return self.cursor.fetchall() if isALL else self.cursor.fetchone()

    def show(self, sql, kwargs):
        print("-" * 30)
        print("the sql is {}, the kwargs is{}".format(sql, kwargs))

    def close(self):
        self.db.close()
