import MySQLdb
import json
import difflib
import uuid
import user.lib.print_color as print_color

# 自製uid
def get_uuid():
    uid = uuid.uuid4()
    uid_str = str(uid).replace('-', '')  
    short_uid = uid_str[:12] 
    return short_uid


class SQL:
    def __init__(self, config):
        self.config = config
        self.connect()

    def connect(self):
        self.db = MySQLdb.connect(**self.config)
        self.cursor = self.db.cursor()

    def create_tables(self):
        sql = f'''
            CREATE TABLE IF NOT EXISTS user_social (
                userid VARCHAR(36) NOT NULL PRIMARY KEY,
                email VARCHAR(24) NOT NULL,
                uid VARCHAR(24) NOT NULL
            )
        '''
        self.cursor.execute(sql)

    # 新增使用者並回傳uid
    def insert(self, userid, email):

        uid = self.check_if_email_exists(email)
        if uid is None:
            uid = get_uuid()

        if not self.check_if_userid_exists(userid):
            sql = "INSERT INTO user_social (userid, email, uid) VALUES (%s, %s, %s)"
            data = (userid, email, uid)
            self.cursor.execute(sql, data)
            self.db.commit()

        return uid

    # 檢查是否有此userid
    def check_if_userid_exists(self, userid):
        sql = "SELECT userid FROM user_social WHERE userid = %s"
        self.cursor.execute(sql, (userid,))
        result = self.cursor.fetchone()
        return result
    
    # 檢查是否有此email 回傳uid
    def check_if_email_exists(self, email):
        sql = "SELECT uid FROM user_social WHERE email = %s"
        self.cursor.execute(sql, (email,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def close(self):
        self.db.close()
