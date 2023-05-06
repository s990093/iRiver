import MySQLdb
import json
import difflib


class SQL:
    def __init__(self, config):
        self.config = config
        self.connect()

    def connect(self):
        self.db = MySQLdb.connect(**self.config)
        self.cursor = self.db.cursor()

    def create_tables(self, table_name):

        # Create the artists table
        sql = f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                email VARCHAR(32) NOT NULL PRIMARY KEY,
                phone VARCHAR(32) NOT NULL
            )
        '''
        self.cursor.execute(sql)

    def close(self):
        self.db.close()
