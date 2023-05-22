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
        self.table_name = table_name
        sql = f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                artist VARCHAR(255) NOT NULL,
                title VARCHAR(255) NOT NULL,
                music_ID VARCHAR(255),
                album VARCHAR(255),
                label VARCHAR(255),
                artist_url VARCHAR(255),
                sources VARCHAR(255),
                download_status BOOLEAN DEFAULT FALSE,
                style VARCHAR(255),
                country VARCHAR(255),
                language VARCHAR(255),
                description VARCHAR(255),
                keywords VARCHAR(255),
                ch_lyrics TEXT,
                en_lyrics TEXT,
                rating VARCHAR(255),
                views INT(20),
                release_year INT(10),
                publish_time INT(10),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        '''
        self.cursor.execute(sql)
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

    def insert(self, **kwargs):
        print(**kwargs)

    def updata(self, **kwargs):
        print(**kwargs)

    def select(self, **kwargs):
        print(**kwargs)
    
    def delete(self, **kwargs):
        print(**kwargs)

    def close(self):
        self.db.close()
