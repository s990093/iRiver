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
        sql = f'''
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                music_list INT NOT NULL,
                music_ID VARCHAR(32) NOT NULL,
                favorite VARCHAR(2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        '''
        self.cursor.execute(sql)


    def save_data(self, music_ID_list, music_list=1):
        try:
            # 解析list
            music_ID_list = json.loads(music_ID_list)
            for music_ID in music_ID_list:
                if not music_ID:
                    continue
                # 查询数据库中是否已存在相同的 music_ID
                select_sql = (f'SELECT COUNT(*) FROM {self.table_name} '
                            'WHERE music_ID = %s')
                self.cursor.execute(select_sql, (music_ID,))
                result = self.cursor.fetchone()
                if result[0] == 0:
                    # 不存在则插入新数据
                    insert_sql = (f'INSERT INTO {self.table_name} '
                                '(music_list, music_ID) '
                                'VALUES (%s, %s)')
                    insert_values = (music_list, music_ID)
                    self.cursor.execute(insert_sql, insert_values)
            # 提交事务
            self.db.commit()
            return True
        except Exception as e:
            print(e)
            return False


    
    
    def delete_data(self, music_ID_list, music_list=1):
        try:
            # 解析list
            music_ID_list = json.loads(music_ID_list)
            # 删除每个id
            for music_ID in music_ID_list:
                if not music_ID:
                    continue
                music_list_sql = (f'DELETE FROM {self.table_name} '
                                'WHERE music_list = %s AND music_ID = %s'
                                )
                music_list_values = (music_list, music_ID)
                self.cursor.execute(music_list_sql, music_list_values)
            # 提交更改
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error deleting data: {e}")
            return False


    def get_music_list(self , music_list= 1):
        sql = f'SELECT music_ID FROM {self.table_name} WHERE {music_list} = %s ORDER BY created_at  DESC'
        self.cursor.execute(sql , (music_list, ))
        return self.cursor.fetchall()
        

    def close(self):
        self.db.close()
