import MySQLdb
import json
import difflib
from user.lib.sql.sql_class import SQL as set_sql_class
from user.lib.print_color import print_have_line


class SQL(set_sql_class):
    def __init__(self, config):
        super().__init__(config)

        self.table_name = "user_setting_eq"

    def create_table(self):
        sql = f'''
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                UID_EQ VARCHAR(36) NOT NULL PRIMARY KEY,
                ENGANCE_HIGH BOOL,
                ENGANCE_MIDDLE BOOL,
                ENGANCE_LOW BOOL,
                ENGANCE_HEAVY BOOL,
                STYLE VARCHAR(255),
                EQ_HIGH INT CHECK (EQ_HIGH >= 0 AND EQ_HIGH <= 100),
                EQ_MIDDLE INT CHECK (EQ_MIDDLE >= 0 AND EQ_MIDDLE <= 100),
                EQ_LOW INT CHECK (EQ_LOW >= 0 AND EQ_LOW <= 100),
                EQ_HEAVY INT CHECK (EQ_HEAVY >= 0 AND EQ_HEAVY <= 100),
                EQ_DISTORTION INT CHECK (EQ_DISTORTION >= 0 AND EQ_DISTORTION <= 100),
                EQ_ZIP INT CHECK (EQ_ZIP >= 0 AND EQ_ZIP <= 100),
                SPATIAL_AUDIO VARCHAR(255)
            )
        '''
        self.cursor.execute(sql)

        super().create_table(table_name=self.table_name)

    def commit(self, method: str, **kwargs):
        kwargs = kwargs.get('kwargs')
        if method == "insert":
            return self.tuple_to_dict(data_tuple=self.insert(**kwargs))
        elif method == "update":
            return self.update(**kwargs)
        elif method == "select":
            return self.tuple_to_dict(data_tuple=self.select(**kwargs))
        else:
            print("-"*30)
            print(f"the method {method} is not supported")
            return False

    def insert(self, **kwargs):
        sql = sql = f"INSERT IGNORE INTO {self.table_name} (UID_EQ, ENGANCE_HIGH, ENGANCE_MIDDLE, ENGANCE_LOW, ENGANCE_HEAVY, STYLE, EQ_HIGH, EQ_MIDDLE, EQ_LOW, EQ_HEAVY, EQ_DISTORTION, EQ_ZIP, SPATIAL_AUDIO) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        return super().insert(sql=sql, values=self.dict_to_tuple(**kwargs))

    def update(self, uid, **kwargs):
        sql = f"UPDATE {self.table_name} SET {kwargs['column']} = %s WHERE UID_EQ = %s"
        return super().update(sql=sql, values=(kwargs["new_value"], uid))

    def select(self, **kwargs):
        sql = f'SELECT * FROM {self.table_name} WHERE UID_EQ = %s'
        return super().select(sql=sql, values=(kwargs["UID_EQ"],))

    def regsiter(self, UID_EQ: str):
        self.insert(UID_EQ=UID_EQ,
                    ENGANCE_HIGH=False,
                    ENGANCE_MIDDLE=False,
                    ENGANCE_LOW=False,
                    ENGANCE_HEAVY=False,
                    STYLE="null",
                    EQ_HIGH=50,
                    EQ_MIDDLE=50,
                    EQ_LOW=50,
                    EQ_HEAVY=50,
                    EQ_DISTORTION=0,
                    EQ_ZIP=0,
                    SPATIAL_AUDIO="null"
                    )

    def execute(self, sql, values, isALL=False):
        return super().execute(sql, values, isALL)

    def dict_to_tuple(self, **kwargs):
        return (
            kwargs.get('UID_EQ'),
            kwargs.get('ENGANCE_HIGH'),
            kwargs.get('ENGANCE_MIDDLE'),
            kwargs.get('ENGANCE_LOW'),
            kwargs.get('ENGANCE_HEAVY'),
            kwargs.get('STYLE'),
            kwargs.get('EQ_HIGH'),
            kwargs.get('EQ_MIDDLE'),
            kwargs.get('EQ_LOW'),
            kwargs.get('EQ_HEAVY'),
            kwargs.get('EQ_DISTORTION'),
            kwargs.get('EQ_ZIP'),
            kwargs.get('SPATIAL_AUDIO'),
        )

    def tuple_to_dict(self, data_tuple):
        keys = [
            'UID_EQ',
            'ENGANCE_HIGH',
            'ENGANCE_MIDDLE',
            'ENGANCE_LOW',
            'ENGANCE_HEAVY',
            'STYLE',
            'EQ_HIGH',
            'EQ_MIDDLE',
            'EQ_LOW',
            'EQ_HEAVY',
            'EQ_DISTORTION',
            'EQ_ZIP',
            'SPATIAL_AUDIO'
        ]
        return dict(zip(keys, data_tuple))

    # def get_user_eq(self, UID_EQ):
    #     self.cursor.execute(
    #         'SELECT * FROM user_eq WHERE UID_EQ = %s',
    #         (UID_EQ,)
    #     )
    #     row = self.cursor.fetchone()

    #     if row:
    #         columns = [desc[0] for desc in self.cursor.description]
    #         user_eq = dict(zip(columns, row))
    #         return user_eq
    #     else:
    #         return None
