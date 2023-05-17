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

    def create_tables(self):
        sql = f'''
            CREATE TABLE IF NOT EXISTS user_eq (
                UID VARCHAR(36) NOT NULL PRIMARY KEY,
                ENGANCE_HIGH BOOL,
                ENGANCE_MIDDLE BOOL,
                ENGANCE_LOW BOOL,
                ENGANCE_HEAVY BOOL,
                STYLE_POP BOOL,
                STYLE_R&R BOOL,
                STYLE_JAZZ BOOL,
                STYLE_ELECTRONIC BOOL,
                STYLE_HIP_HOP BOOL,
                EQ_HIGH INT CHECK (EQ_HIGH >= 0 AND EQ_HIGH <= 100),
                EQ_MIDDLE INT CHECK (EQ_MIDDLE >= 0 AND EQ_MIDDLE <= 100),
                EQ_LOW INT CHECK (EQ_LOW >= 0 AND EQ_LOW <= 100),
                EQ_HEAVY INT CHECK (EQ_HEAVY >= 0 AND EQ_HEAVY <= 100),
                EQ_DISTORTION INT CHECK (EQ_DISTORTION >= 0 AND EQ_DISTORTION <= 100),
                EQ_ZIP INT CHECK (EQ_ZIP >= 0 AND EQ_ZIP <= 100),
                FRONT_GUITAR BOOL,
                FRONT_VOCAL BOOL,
                FRONT_DRUM BOOL,
                FRONT_BASS BOOL
            )
        '''
        self.cursor.execute(sql)

    def save_user_eq(self, **user_data): 
        UID = user_data.get('UID')
        ENGANCE_HIGH = user_data.get('ENGANCE_HIGH')
        ENGANCE_MIDDLE = user_data.get('ENGANCE_MIDDLE')
        ENGANCE_LOW = user_data.get('ENGANCE_LOW')
        ENGANCE_HEAVY = user_data.get('ENGANCE_HEAVY')
        STYLE_POP = user_data.get('STYLE_POP')
        STYLE_RR = user_data.get('STYLE_R&R')
        STYLE_JAZZ = user_data.get('STYLE_JAZZ')
        STYLE_ELECTRONIC = user_data.get('STYLE_ELECTRONIC')
        STYLE_HIP_HOP = user_data.get('STYLE_HIP_HOP')
        EQ_HIGH = user_data.get('EQ_HIGH')
        EQ_MIDDLE = user_data.get('EQ_MIDDLE')
        EQ_LOW = user_data.get('EQ_LOW')
        EQ_HEAVY = user_data.get('EQ_HEAVY')
        EQ_DISTORTION = user_data.get('EQ_DISTORTION')
        EQ_ZIP = user_data.get('EQ_ZIP')
        FRONT_GUITAR = user_data.get('FRONT_GUITAR')
        FRONT_VOCAL = user_data.get('FRONT_VOCAL')
        FRONT_DRUM = user_data.get('FRONT_DRUM')
        FRONT_BASS = user_data.get('FRONT_BASS')

        self.cursor.execute(
            'INSERT IGNORE INTO user_eq (UID, ENGANCE_HIGH, ENGANCE_MIDDLE, ENGANCE_LOW, ENGANCE_HEAVY, STYLE_POP, STYLE_R&R, STYLE_JAZZ, STYLE_ELECTRONIC, STYLE_HIP_HOP, EQ_HIGH, EQ_MIDDLE, EQ_LOW, EQ_HEAVY, EQ_DISTORTION, EQ_ZIP, FRONT_GUITAR, FRONT_VOCAL, FRONT_DRUM, FRONT_BASS) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (UID, ENGANCE_HIGH, ENGANCE_MIDDLE, ENGANCE_LOW, ENGANCE_HEAVY, STYLE_POP, STYLE_RR, STYLE_JAZZ, STYLE_ELECTRONIC, STYLE_HIP_HOP, EQ_HIGH, EQ_MIDDLE, EQ_LOW, EQ_HEAVY, EQ_DISTORTION, EQ_ZIP, FRONT_GUITAR, FRONT_VOCAL, FRONT_DRUM, FRONT_BASS)
        )

        self.cursor.execute(
            'UPDATE user_eq SET ENGANCE_HIGH=%s, ENGANCE_MIDDLE=%s, ENGANCE_LOW=%s, ENGANCE_HEAVY=%s, STYLE_POP=%s, STYLE_R&R=%s, STYLE_JAZZ=%s, STYLE_ELECTRONIC=%s, STYLE_HIP_HOP=%s, EQ_HIGH=%s, EQ_MIDDLE=%s, EQ_LOW=%s, EQ_HEAVY=%s, EQ_DISTORTION=%s, EQ_ZIP=%s, FRONT_GUITAR=%s, FRONT_VOCAL=%s, FRONT_DRUM=%s, FRONT_BASS=%s WHERE UID=%s',
            (ENGANCE_HIGH, ENGANCE_MIDDLE, ENGANCE_LOW, ENGANCE_HEAVY, STYLE_POP, STYLE_RR, STYLE_JAZZ, STYLE_ELECTRONIC, STYLE_HIP_HOP, EQ_HIGH, EQ_MIDDLE, EQ_LOW, EQ_HEAVY, EQ_DISTORTION, EQ_ZIP, FRONT_GUITAR, FRONT_VOCAL, FRONT_DRUM, FRONT_BASS, UID)
        )

        self.db.commit()

        
    def close(self):
        self.db.close()
