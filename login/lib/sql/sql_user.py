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
                email VARCHAR(100) NOT NULL PRIMARY KEY,
                username VARCHAR(100) NOT NULL,
                phone VARCHAR(20) NOT NULL,
                country CHAR(2),
                birthday DATE
            )
        '''
        self.cursor.execute(sql)

    def save_user_data(self, tabel_name, email, username, phone, country, birthday):
        print(tabel_name)
        self.cursor.execute(f'INSERT IGNORE INTO {tabel_name} (email, username, phone, country, birthday) VALUES ("{email}", "{username}", "{phone}", "{country}", "{birthday}")')
        self.cursor.execute(f'UPDATE {tabel_name} SET username="{username}", phone="{phone}", country="{country}", birthday="{birthday}" WHERE email="{email}"')
        self.db.commit()

    def close(self):
        self.db.close()
