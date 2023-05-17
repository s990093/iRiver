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
                id VARCHAR(36) NOT NULL PRIMARY KEY,
                email VARCHAR(24) NOT NULL,
                username VARCHAR(24) NOT NULL,
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
        id = user_profile.get('id')
        email = user_profile.get('email')
        username = user_profile.get('username')
        phone = user_profile.get('phone')
        country = user_profile.get('country')
        birthday = user_profile.get('birthday')
        test = user_profile.get('test', 0)
        level = user_profile.get('level', 0)
        self.cursor.execute(
            'INSERT IGNORE INTO user_profile (id, email, username, phone, country, birthday, test, level) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            (id, email, username, phone, country, birthday, test, level)
        )
        self.cursor.execute(
            'UPDATE user_profile SET email=%s, username=%s, phone=%s, country=%s, birthday=%s, test=%s, level=%s WHERE id=%s',
            (email, username, phone, country, birthday, test, level, id)
        )
        self.db.commit()

    def get_user_data(self,uid):
        self.cursor.execute(
            'SELECT * FROM user_profile WHERE id=%s',
            (uid,)
        )
        result = self.cursor.fetchone()
        if result:
            data = {
                'id': result[0],
                'email': result[1],
                'username': result[2],
                'phone': result[3],
                'country': result[4],
                'birthday': result[5],
                'test': result[6],
                'level': result[7],
            }
            print("$"*30)
            print(data)
            return data
        else:
            return None
    def get_user_show_data(self,uid):
        self.cursor.execute(
            'SELECT * FROM user_profile WHERE id=%s',
            (uid,)
        )
        result = self.cursor.fetchone()
        if result:
            data = {
                'id': result[0],
                'email': result[1],
                'username': result[2],
                'level': result[7],
            }
            print("$"*30)
            print(data)
            return data
        else:
            return None
        
    def close(self):
        self.db.close()
