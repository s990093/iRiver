import MySQLdb
import json
import difflib
from user.lib.sql.sql_class import SQL as set_sql_class


class SQL(set_sql_class):
    def __init__(self, config):
        super().__init__(config)

        self.table_name = "user_setting"

    def create_table(self):
        sql = f'''
           CREATE TABLE IF NOT EXISTS {self.table_name} (
                UID_SETTING VARCHAR(36) NOT NULL PRIMARY KEY,
                LANGUAGE VARCHAR(255) NOT NULL,
                SHOW_MODAL VARCHAR(255) NOT NULL,
                AUDIO_QUALITY VARCHAR(255) NOT NULL,
                AUDIO_AUTO_PLAY BOOL NOT NULL,
                WIFI_AUTO_DOWNLOAD BOOL NOT NULL,
                CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        '''
        self.cursor.execute(sql)

        super().create_table(table_name=self.table_name)

    def commit(self, method: str, **kwargs):
        if method == "insert":
            return self.tuple_to_dict(data_tuple=self.insert(**kwargs))
        elif method == "update":
            return self.tuple_to_dict(data_tuple=self.update(**kwargs))
        elif method == "select":
            return self.tuple_to_dict(data_tuple=self.select(**kwargs))
        else:
            print("-"*30)
            print(f"the method {method} is not supported")
            return False

    def insert(self, **kwargs):
        sql = f'INSERT INTO {self.table_name} (UID_SETTING, LANGUAGE, SHOW_MODAL, AUDIO_QUALITY, AUDIO_AUTO_PLAY, WIFI_AUTO_DOWNLOAD) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE UID_SETTING = UID_SETTING'
        return super().insert(sql=sql, values=self.dict_to_tuple(**kwargs))

    def select(self, **kwargs):
        sql = f'SELECT UID_SETTING, LANGUAGE, SHOW_MODAL, AUDIO_QUALITY, AUDIO_AUTO_PLAY, WIFI_AUTO_DOWNLOAD FROM {self.table_name} WHERE UID_SETTING = %s'
        return super().select(sql=sql, values=(kwargs["UID_SETTING"],))

    def regsiter(self, UID_SETTING: str):
        self.insert(UID_SETTING=UID_SETTING,
                    LANGUAGE="ch",
                    SHOW_MODAL="auto",
                    AUDIO_QUALITY="auto",
                    AUDIO_AUTO_PLAY="auto",
                    WIFI_AUTO_DOWNLOAD="auto"
                    )

    def execute(self, sql, values, isALL=False):
        return super().execute(sql, values, isALL)

    def dict_to_tuple(self, **kwargs):
        return (
            kwargs.get('UID_SETTING'),
            kwargs.get('LANGUAGE'),
            kwargs.get('SHOW_MODAL'),
            kwargs.get('AUDIO_QUALITY'),
            kwargs.get('AUDIO_AUTO_PLAY'),
            kwargs.get('WIFI_AUTO_DOWNLOAD'),
        )

    def tuple_to_dict(self ,data_tuple):
        keys = [
            'UID_SETTING',
            'LANGUAGE',
            'SHOW_MODAL',
            'AUDIO_QUALITY',
            'AUDIO_AUTO_PLAY',
            'WIFI_AUTO_DOWNLOAD'
        ]
        return dict(zip(keys, data_tuple))
