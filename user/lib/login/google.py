import uuid
import requests
from user.lib.login.base import base

client_id = '1026795084542-4faa7ard63anna4utjtmavuvbe4t4mf4.apps.googleusercontent.com'
redirect_uri = 'http://127.0.0.1:8000/complete/google/'
client_secret = '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'
scope = 'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email'
access_type = 'offline'
include_granted_scopes = 'true'
response_type = 'code'

def google_url(request):
    state = str(uuid.uuid4())
    request.session['oauth_state'] = state
    auth_url = f'https://accounts.google.com/o/oauth2/v2/auth?scope={scope}&access_type={access_type}&include_granted_scopes={include_granted_scopes}&response_type={response_type}&state={state}&redirect_uri={redirect_uri}&client_id={client_id}'
    return auth_url


# 取得存取令牌
def google_token(code):
    url = 'https://oauth2.googleapis.com/token'
    params = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }
    response = requests.post(url, data=params)
    token_data = response.json()
    id_token = token_data.get('id_token', None)
    access_token = token_data.get('access_token', None)
    return{'id_token': id_token, 'access_token': access_token}


def google_profile(id_token):
    url = 'https://oauth2.googleapis.com/tokeninfo'
    data = {
        'id_token': id_token,
    }
    response = requests.get(url, params=data)
    data = response.json()
    email = data['email']
    picture = data['picture']
    userid = data['sub']
    name = data['name']
    return {'email': email, 'picture': picture, 'userid': userid, 'name': name}


# 取得回傳資料
def google_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    if code and state==request.session.get('oauth_state'):
        token_data = google_token(code)
        id_token = token_data['id_token']
        access_token = token_data['access_token']
        userdata = google_profile(id_token)
        name = userdata['name']
        email = userdata['email']
        picture = userdata['picture']
        userid = userdata['userid']
        base(name=name, email=email, picture=picture, userid=userid,request=request)
        return True
    print("驗證失敗")
    return False