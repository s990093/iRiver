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
        sql = f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                email VARCHAR(36) NOT NULL PRIMARY KEY,
                username VARCHAR(36) NOT NULL,
                phone VARCHAR(16) NOT NULL,
                country CHAR(2),
                birthday DATE,
                test TINYINT(2) UNSIGNED DEFAULT 0,
                level TINYINT(2) UNSIGNED DEFAULT 0
            )
        '''
        self.cursor.execute(sql)


    def save_user_data(self, **user_data):
        email = user_data.get('email')
        username = user_data.get('username')
        phone = user_data.get('phone')
        country = user_data.get('country')
        birthday = user_data.get('birthday')
        test = user_data.get('test', 0)
        level = user_data.get('level', 0)
        self.cursor.execute(
            'INSERT IGNORE INTO user (email, username, phone, country, birthday, test, level) VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (email, username, phone, country, birthday, test, level)
        )
        self.cursor.execute(
            'UPDATE user SET username=%s, phone=%s, country=%s, birthday=%s, test=%s, level=%s WHERE email=%s',
            (username, phone, country, birthday, test, level, email)
        )
        self.db.commit()


    def close(self):
        self.db.close()
