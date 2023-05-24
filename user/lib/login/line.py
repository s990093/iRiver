import uuid
import requests
from user.lib.login.base import base
client_id = '1661190797'
redirect_uri = 'http://127.0.0.1:8000/complete/line/'
client_secret = '3fc12add18f596c2597c993f1f858acf'


def line_url(request):
    state = str(uuid.uuid4())
    request.session['oauth_state'] = state
    auth_url = f'https://access.line.me/oauth2/v2.1/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&state={state}&scope=profile%20openid%20email'
    return auth_url


# 取得存取令牌
def line_token(code):
    url = 'https://api.line.me/oauth2/v2.1/token'
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret,
    }
    response = requests.post(url,data)
    token_data = response.json()
    id_token = token_data.get('id_token', None)
    access_token = token_data.get('access_token', None)
    return{'id_token': id_token, 'access_token': access_token}


def line_profile2(id_token, client_id):
    url = 'https://api.line.me/oauth2/v2.1/verify'
    data = {
        'id_token': id_token,
        'client_id': client_id,
    }
    response = requests.post(url, data=data)
    data = response.json()
    email = data['email']
    picture = data['picture']
    userid = data['sub']
    name = data['name']
    return {'email': email, 'picture': picture, 'userid': userid, 'name': name}

def line_profile(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://api.line.me/v2/profile', headers=headers)
    if response.status_code == 200:
        data = response.json()
        username = data['displayName']
        userId = data['userId']
        return {'username': username, 'userId': userId}
    print("獲取用戶資料失敗")
    return None

# 取得回傳資料
def line_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    if code and state==request.session.get('oauth_state'):
        token_data = line_token(code)
        id_token = token_data['id_token']
        access_token = token_data['access_token']
        userdata = line_profile2(id_token, client_id)
        name = userdata['name']
        email = userdata['email']
        picture = userdata['picture']
        userid = userdata['userid']
        base(name=name, email=email, picture=picture, userid=userid,request=request)
        return{'name': name, 'email': email, 'picture': picture, 'userid': userid, 'access_token': access_token}
    print("驗證失敗")
    return None