import MySQLdb
import json
import difflib


class SQL:
    def __init__(self, config, table_name):
        '''table'''
        self.table_name = table_name
        self.config = config
        self.connect()

    def connect(self):
        self.db = MySQLdb.connect(**self.config)
        self.cursor = self.db.cursor()

    def create_tables(self):
        # Create the table
        sql = f'''
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                music_list INT NOT NULL,
                music_ID VARCHAR(32) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        '''
        self.cursor.execute(sql)


    def save_data(self, music_ID_list,  music_list=1):
        music_ID_list = json.loads(music_ID_list)

        for music_ID in music_ID_list:
            if not music_ID:
                continue
            music_list_sql = (f'INSERT INTO {self.table_name} '
                              '(music_list , music_ID) '
                              'VALUES (%s, %s)'
                              )
            music_list_values = (music_list, music_ID)
            self.cursor.execute(music_list_sql, music_list_values)

        self.db.commit()
        print('=' * 30)
        print('save data')
    
    def get_music_list(self , music_list= 1):
        sql = f'SELECT music_ID FROM {self.table_name} WHERE {music_list} = %s ORDER BY created_at  DESC'
        self.cursor.execute(sql , (music_list, ))
        
        return self.cursor.fetchall()
        

    def close(self):
        self.db.close()
