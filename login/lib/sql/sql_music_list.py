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
                favorite BOOLEAN NOT NULL DEFAULT false,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        '''
        self.cursor.execute(sql)
    
    def set_all_favorite(self, music_id, value):
        sql = f'UPDATE {self.table_name} SET favorite = %s WHERE music_ID = %s'
        self.cursor.execute(sql, (value, music_id))
        self.db.commit()

    def save_data(self, music_ID_list, music_list ):
        """1  我的最愛"""
        try:
            # 解析list
            music_ID_list = json.loads(music_ID_list)
            for music_ID in music_ID_list:
                if music_list == 1:
                    favorite = True
                    self.set_all_favorite(True)
                else:
                    favorite = self.cheak_ID_in_1(music_ID)

                # 查询数据库中是否已存在相同的 music_ID
                select_sql = (f'SELECT COUNT(*) FROM {self.table_name} ''WHERE music_ID = %s AND music_list = %s')
                self.cursor.execute(select_sql, (music_ID, music_list))
                result = self.cursor.fetchone()
                if result[0] == 0:
                    # 不存在则插入新数据
                    insert_sql = (f'INSERT INTO {self.table_name} '
                                '(music_list, music_ID , favorite) '
                                'VALUES (%s, %s , %s)')
                    insert_values = (music_list, music_ID , favorite)
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
                if music_list == 1:
                    self.set_all_favorite(False)
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
        
    def setfavorite(self, music_ID_list):
        music_ID_list = json.loads(music_ID_list)
        for music_ID in music_ID_list:
            if self.cheak_ID_in_1(music_ID) == False:
                self.save_data(music_ID, 1)
                self.set_all_favorite(music_ID,True)
            current_favorite = self.get_music_info(music_ID)['favorite']
            current_favorite = not current_favorite  # 把 current_favorite 取反
            sql = f'UPDATE {self.table_name} SET favorite = %s WHERE music_ID = %s'
            try:
                self.cursor.execute(sql, (current_favorite, music_ID))  # 把 value 改成 current_favorite
                self.db.commit()
            except:
                return False
        return True 


    def cheak_ID_in_1(self, music_ID):
        sql = f'SELECT * FROM {self.table_name} WHERE music_ID = %s AND music_list = 1'
        self.cursor.execute(sql, (music_ID,))
        result = self.cursor.fetchone()
        if result:
            return True
        else:
            return False

    def close(self):
        self.db.close()

   