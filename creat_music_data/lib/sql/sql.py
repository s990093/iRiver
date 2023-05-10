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
                artist VARCHAR(255) NOT NULL,
                summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
                views INT(20),
                release_year INT(4),
                publish_time INT(10),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        '''
        self.cursor.execute(sql)
        
    def save_data(self, song_infos , summary = None):
        """push data"""
        # Load song_infos into a list
        song_infos_list = json.loads(song_infos)
        style = self.get_style(music_ID= song_infos_list[0]['style'])
        
        if not song_infos_list[0]['style'] == "null" or None:
            style += f",{song_infos_list[0]['style']}"
        
        # Iterate through the list of song infos
        for song_info in song_infos_list:
            # Skip the current iteration if song_infos_list[i] is empty
            if not song_info:
                continue
            select_sql = 'SELECT * FROM artists WHERE artist = %s'
            select_values = (song_info['artist'], )
            self.cursor.execute(select_sql, select_values)
            result = self.cursor.fetchone()

            if not result:
                # Insert data into the artists table if it doesn't exist
                artist_sql = 'INSERT INTO artists (artist , summary) VALUES (%s , %s)'
                artist_values = (song_info['artist'], summary)
                self.cursor.execute(artist_sql, artist_values)

            # Check if the song already exists in the songs table
            select_sql = 'SELECT * FROM songs WHERE music_ID = %s'
            select_values = (song_info['music_ID'], )
            self.cursor.execute(select_sql, select_values)
            result = self.cursor.fetchone()

            if not result:
                # Insert data into the songs table if it doesn't exist
                song_sql = ('INSERT INTO songs '
                            '(artist, title, music_ID, album, label, artist_url, sources, download_status, style, country, language, description, keywords, ch_lyrics, en_lyrics, release_year, publish_time) '
                            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
                song_values = ( song_info['artist'],
                                song_info['title'],
                                song_info['music_ID'],
                                song_info['album'],
                                song_info['label'],
                                song_info['artist_url'],
                                song_info['sources'],
                                song_info['download_status'],
                                style,
                                song_info['country'],
                                song_info['language'],
                                song_info['description'],
                                ','.join(song_info['keywords']),
                                song_info['ch_lyrics'],
                                song_info['en_lyrics'],
                                song_info['release_year'],
                                song_info['publish_time']
                                )
                self.cursor.execute(song_sql, song_values)

        # Commit the transaction
        self.db.commit()
        print('=' * 30)
        print('save data')

    def get_style(self , music_ID):
        sql = 'SELECT style FROM songs WHERE music_ID = %s'
        self.cursor.execute(sql , (music_ID, ))
        return self.cursor.fetchone()
        
    def save_summary(self, artist: str, summary: str):
        update_sql = 'UPDATE artists SET summary = %s WHERE artist = %s'
        update_values = (summary, artist)
        self.cursor.execute(update_sql, update_values)
        self.db.commit()

        

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
        rows = self.cursor.fetchall()
        music_list_infos = []
        for row in rows:
               music_list_infos.append({
                    'artist': row[1],
                    'title': row[2],
                    'music_ID': row[3],
                    'artist_url': row[4],
                    'keywords': row[5],
                    'views': row[6],
                    'publish_time': row[7]
                })
        return  music_list_infos
    
    def get_artist_summary(self , artist :str) ->str :
        sql = 'SELECT summary FROM artists WHERE artist = %s '
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
    
    def get_music_list_infos(self, music_ID_list):
        song_infos = []
        for music_ID in music_ID_list:
            sql = 'SELECT * FROM songs WHERE music_ID = %s'
            self.cursor.execute(sql , (music_ID, ))
            rows = self.cursor.fetchall()
            for row in rows:
                song_infos.append({
                    'artist': row[1],
                    'title': row[2],
                    'music_ID': row[3],
                    'artist_url': row[4],
                    'keywords': row[5],
                    'views': row[6],
                    'publish_time': row[7]
                })
        return song_infos


    def close(self):
        self.db.close()
