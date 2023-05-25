import json
from django.http import HttpResponse
import jwt
import requests


def decode_id_token(id_token, channel_secret):
    id_token_bytes = id_token.encode('utf-8')  # 将 id_token 转换为字节类型
    decoded = jwt.decode(id_token_bytes, channel_secret, algorithms=[
                         'HS256'], options={"verify_signature": False})
    return decoded


def get_line_user_email(access_token, channel_secret):
    id_token = get_id_token(access_token)
    decoded_id_token = decode_id_token(id_token, channel_secret)
    user_email = decoded_id_token.get('email')
    return user_email


def get_id_token(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.post(
        'https://api.line.me/oauth2/v2.1/verify', headers=headers)
    verify_data = response.json()
    print("*"*20)
    print(verify_data)
    id_token = verify_data.get('id_token')
    return id_token

# 以上皆為測試中


def get_line_data(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get('https://api.line.me/v2/profile', headers=headers)
    data = response.json()
    return data


def get_google_data(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'personFields': 'photos'}
    response = requests.get(
        'https://people.googleapis.com/v1/people/me', headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    return None


def get_avatar_url(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'personFields': 'photos'}
    response = requests.get(
        'https://people.googleapis.com/v1/people/me', headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        photos = data.get('photos', [])
        if photos:
            avatar_url = photos[0].get('url')
            return avatar_url
    return None


def get_user_show_data(request):
    if request.method != 'POST':
        return HttpResponse('error')
    # if request.session['user_data'] is None:
    #     session.save_session(request=request , uid= )
    return HttpResponse(json.dumps({
        "success": True,
        "user_data": request.session['user_data'],
        "user_playlists": request.session['user_playlist'],
    }))



