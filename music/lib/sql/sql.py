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
        # Create the artists table
        sql = '''
            CREATE TABLE IF NOT EXISTS artists (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                artist VARCHAR(255) NOT NULL
            )
        '''
        self.cursor.execute(sql)

        # Create the songs table
        sql = '''
            CREATE TABLE IF NOT EXISTS songs (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                artist VARCHAR(255) NOT NULL,
                title VARCHAR(255) NOT NULL,
                music_ID VARCHAR(255),
                artist_url VARCHAR(255),
                keywords VARCHAR(255),
                views INT,
                publish_time INT(10)
            )
        '''
        self.cursor.execute(sql)
        
    def save_data(self, song_infos):
        song_infos_lsit =  json.loads(song_infos) 
        # print(type(song_infos_lsit))
        # print(song_infos_lsit[0]['artist'])
        for i in range(len(song_infos_lsit)):
            if not song_infos_lsit[i]:  # 如果song_infos_lsit[i]是空的，則跳過當前迭代
             continue     
            # Check if the artist already exists in the artists table
            print(f'save {song_infos_lsit[i]["music_ID"]}')
            select_sql = 'SELECT * FROM artists WHERE artist = %s'
            select_values = (song_infos_lsit[i]['artist'], )
            self.cursor.execute(select_sql , select_values)
            result = self.cursor.fetchone()

            if not result:
                # Insert data into the artists table if it doesn't exist
                artist_sql = 'INSERT INTO artists (artist) VALUES (%s)'
                artist_values = (song_infos_lsit[i]['artist'], )
                self.cursor.execute(artist_sql , artist_values)

            # Check if the song already exists in the songs table
            select_sql = 'SELECT * FROM songs WHERE music_ID = %s'
            select_values = (song_infos_lsit[i]['music_ID'], )
            self.cursor.execute(select_sql , select_values)
            result = self.cursor.fetchone()

            if not result:
                # Insert data into the songs table if it doesn't exist
                song_sql = 'INSERT INTO songs (artist, title, music_ID, artist_url, keywords, views, publish_time) VALUES (%s, %s, %s, %s, %s, %s, %s)'
                song_values = (song_infos_lsit[i]['artist'],
                               song_infos_lsit[i]['title'],
                               song_infos_lsit[i]['music_ID'],
                               song_infos_lsit[i]['artist_url'],
                            ','.join(song_infos_lsit[i]['keywords']),
                                song_infos_lsit[i]['views'], 
                                song_infos_lsit[i]['publish_time'])
                
                self.cursor.execute(song_sql, song_values)
            # Commit the transactiony
        self.db.commit()
        print('='*30)
        print('save data')
    
   
    def get_all_song(self, field='*'):
        sql = f'SELECT {field} FROM songs ORDER BY publish_time ASC'
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def get_all_artist(self):
        sql = 'SELECT * FROM artists'
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def get_all_artist_song(self , artist):
        sql = 'SELECT * FROM songs WHERE artist = %s ORDER BY views DESC'
        self.cursor.execute(sql , (artist, ))
        return self.cursor.fetchall()
        
    # 重要

    def query(self, query):
        artist_song_res , artist_song_sorce = self.query_all_artist_song(artist=query) or (None,0)
        song_res        , song_score = self.query_song(song_name=query) or (None, 0)
        
        if(artist_song_sorce > song_score):
            forwards = artist_song_res
            back = song_res
        else:
            forwards = song_res
            back = artist_song_res
        
        result = []
        if forwards is not None:
            result.extend(forwards)
        if back is not None:
            result.extend(back)
 
        return tuple(result)



    def query_all_artist_song(self, artist):
        r =self.get_all_artist()
        try :
            matches = difflib.get_close_matches(artist, [x[1] for x in r], n=3, cutoff=0.4)
            score = difflib.SequenceMatcher(None, artist, matches[0]).ratio()
        except Exception as e:
            # print(e)
            return None , 0
        if matches is None:
            return None , 0
            
        result = []
        count = 0
        for match in matches:
                sql = 'SELECT * FROM songs WHERE artist = %s ORDER BY views DESC LIMIT 4'
                self.cursor.execute(sql, (match,))
                matched_songs = self.cursor.fetchall()
                if matched_songs:
                    result.extend(matched_songs)
                    break
                if count >= 3:
                    break
        return result, score
    

    def query_song(self , song_name):
        r = self.get_all_song(field='title')
        try:
            matches = difflib.get_close_matches(song_name, [x[0] for x in r],n= 3, cutoff=0.0003)
            score = difflib.SequenceMatcher(None, song_name, matches[0]).ratio()
            # print('*'*20)
            # print(f'get_song sorce{score}')
        except Exception as e:
            print(e)
            return None ,0
        if not matches:
            return None ,0
        result = []
        count = 0
        for match in matches:
            sql = 'SELECT * FROM songs WHERE title = %s ORDER BY views DESC  LIMIT 4'
            self.cursor.execute(sql, (match,))
            matched_songs = self.cursor.fetchall()
            if matched_songs:
                result.extend(matched_songs)
                break
            if count >= 3:
                break
        return result, score

    # def get_song_url(self , song_url):
    def close(self):
        self.db.close()
