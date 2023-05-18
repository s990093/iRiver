from music.lib.sql.sql_class import SQL as SQLClass


class SQL(SQLClass):
    def __init__(self, config):
        super().__init__(config)
        self.table_name = "hot"
