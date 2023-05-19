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

    def close(self):
        self.db.close()

    def get_extra_data(self, uid):
        self.cursor.execute(
            'SELECT extra_data FROM social_auth_usersocialauth WHERE uid = %s',
            (uid,)
        )
        result = self.cursor.fetchone()
        if result:
            extra_data = result[0]
            return extra_data
        else:
            return None
