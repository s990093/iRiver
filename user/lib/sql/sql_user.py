import MySQLdb
import json
import difflib
# 123132


class SQL:
    def __init__(self, config):
        self.config = config
        self.connect()

    def connect(self):
        self.db = MySQLdb.connect(**self.config)
        self.cursor = self.db.cursor()

    def create_tables(self):
        sql = f'''
            CREATE TABLE IF NOT EXISTS user_profile (
                id VARCHAR(255) NOT NULL PRIMARY KEY,
                email VARCHAR(36) NOT NULL,
                username VARCHAR(36) NOT NULL,
                phone VARCHAR(16) NOT NULL,
                country CHAR(2),
                birthday DATE,
                test TINYINT(2) UNSIGNED DEFAULT 0,
                level TINYINT(2) UNSIGNED DEFAULT 0
            )
        '''
        self.cursor.execute(sql)

    def save_user_profile(self, **user_profile):
        print("*"*30)
        print(user_profile)
        key = user_profile.get('key')
        email = user_profile.get('email')
        username = user_profile.get('username')
        phone = user_profile.get('phone')
        country = user_profile.get('country')
        birthday = user_profile.get('birthday')
        test = user_profile.get('test', 0)
        level = user_profile.get('level', 0)
        self.cursor.execute(
            'INSERT IGNORE INTO user_profile (id, email, username, phone, country, birthday, test, level) VALUES (%s, %s, %s, %s, %s, %s, %s , %s)',
            (key, email, username, phone, country, birthday, test, level)
        )
        self.cursor.execute(
            'UPDATE user_profile SET email=%s, username=%s, phone=%s, country=%s, birthday=%s, test=%s, level=%s WHERE id=%s',
            (email, username, phone, country, birthday, test, level, key)
        )
        self.db.commit()

    def close(self):
        self.db.close()
