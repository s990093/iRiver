import uuid
import requests
from user.lib.login.base import base
import urllib.parse

test = False
client_id = '1661190797'
client_secret = '3fc12add18f596c2597c993f1f858acf'
response_type = 'code'
scopes = ["profile", "openid", "email"]
if (test==True):
    redirect_uri = 'http://127.0.0.1:8000/complete/line/'
else:
    redirect_uri = 'https://iriver.ddns.net/complete/line/'


#生成登入連結
def line_url(request):
    state = str(uuid.uuid4())
    request.session['oauth_state'] = state
    encoded_scopes = urllib.parse.quote(" ".join(scopes))
    auth_url = f'https://access.line.me/oauth2/v2.1/authorize?response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&state={state}&scope={encoded_scopes}'
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
    response = requests.post(url, data)
    token_data = response.json()
    id_token = token_data.get('id_token', None)
    access_token = token_data.get('access_token', None)
    return {'id_token': id_token, 'access_token': access_token}


# 取得用戶資料
def line_profile(id_token, client_id):
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

# 回傳資料處理
def line_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    if code and state == request.session.get('oauth_state'):
        token_data = line_token(code)
        id_token = token_data['id_token']
        access_token = token_data['access_token']
        userdata = line_profile(id_token, client_id)
        name = userdata['name']
        email = userdata['email']
        picture = userdata['picture']
        userid = userdata['userid']
        base(
            name=name, 
            email=email, 
            user_img_url=picture,
            userid=userid, 
            request=request)
        return True
    print("驗證失敗")
    return False
