import MySQLdb
import json
import difflib


class SQL:
    def __init__(self, config, table_name :str):
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
                favorite BOOLEAN NOT NULL DEFAULT false,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        '''
        self.cursor.execute(sql)
    def get_music_list(self , music_list= 1):
        sql = f'SELECT music_ID FROM {self.table_name} WHERE music_list = %s ORDER BY created_at  DESC'
        self.cursor.execute(sql , (music_list, ))
        return self.cursor.fetchall() 
    


    def save_data(self, music_ID_list, music_list):
        """1  我的最愛"""
        try:
            music_ID_list = json.loads(music_ID_list)
            for music_ID in music_ID_list:
                print("add ",music_ID ," => ",  music_list )
                # 查询数据库中是否已存在相同的 music_ID
                select_sql = (f'SELECT COUNT(*) FROM {self.table_name} ''WHERE music_ID = %s AND music_list = %s')
                self.cursor.execute(select_sql, (music_ID, music_list))
                result = self.cursor.fetchone()
                if result[0] == 0:
                    # 不存在则插入新数据
                    insert_sql = (f'INSERT INTO {self.table_name} '
                                '(music_list, music_ID , favorite) '
                                'VALUES (%s, %s , %s)')
                    insert_values = (music_list, music_ID , False)
                    self.cursor.execute(insert_sql, insert_values)
                # 如果是我的最愛或在最愛裡面，則將favorite設為true    
                if music_list == 1 or self.check_ID_in_1(music_ID) == True:
                    self.set_all_favorite(music_ID ,True)
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
                music_list_sql = (f'DELETE FROM {self.table_name} '
                                'WHERE music_list = %s AND music_ID = %s'
                                )
                music_list_values = (music_list, music_ID)
                self.cursor.execute(music_list_sql, music_list_values)
                # 如果是我的最愛，則將favorite設為false
                if music_list == 1:
                    self.set_all_favorite(music_ID , False)
            # 提交更改
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error deleting data: {e}")
            return False


    def setfavorite(self, music_ID_list):
        music_ID_list = json.loads(music_ID_list)
        for music_ID in music_ID_list:
            self.save_data(music_ID, 1)

    def check_ID_in_1(self, music_ID):
        sql = f'SELECT * FROM {self.table_name} WHERE music_ID = %s AND music_list = 1'
        self.cursor.execute(sql, (music_ID ,))
        result = self.cursor.fetchone()
        if result: 
            return True
        else:
            return False
    
    
    def set_all_favorite(self, music_id, value):
        sql = f'UPDATE {self.table_name} SET favorite = %s WHERE music_ID = %s'
        self.cursor.execute(sql, (value, music_id))
        self.db.commit()
    
    def get_playlists(self , email):
        sql = f'SELECT COUNT(*) FROM {email}'
        self.cursor.execute(sql, (email ,))
        return self.cursor.fetchall() 



    def close(self):
        self.db.close()

   