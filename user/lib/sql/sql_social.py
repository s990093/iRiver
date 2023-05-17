import MySQLdb
import json
import difflib
import requests

def get_avatar_url(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'personFields': 'photos'}
    response = requests.get('https://people.googleapis.com/v1/people/me', headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        photos = data.get('photos', [])
        
        if photos:
            avatar_url = photos[0].get('url')
            return avatar_url
    
    return None

class SQL:
    def __init__(self, config):
        self.config = config
        self.connect()

    def connect(self):
        self.db = MySQLdb.connect(**self.config)
        self.cursor = self.db.cursor()
    
    def close(self):
        self.db.close()

    def get_extra_data(self, uid):
        self.cursor.execute(
            'SELECT extra_data FROM social_auth_usersocialauth WHERE uid = %s',
            (uid,)
        )
        result = self.cursor.fetchone()
        if result:
            extra_data = result[0]
            return extra_data
        else:
            return None

    