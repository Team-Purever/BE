# 카카오 인증 코드를 사용하여 액세스 토큰을 교환하고 사용자 정보를 가져오는 유틸리티 함수 정의

import requests
import os
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
import urllib.parse
from .models import User


class KakaoAccessTokenException(Exception):
    pass
class NaverAccessTokenException(Exception):
    pass
class GoogleAccessTokenException(Exception):
    pass


def exchange_kakao_access_token(access_code):
    response = requests.post(
        'https://kauth.kakao.com/oauth/token',
        headers={
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',    
        },
        data={
            'grant_type': 'authorization_code',
            'client_id': os.environ.get('KAKAO_REST_API_KEY'),
            'client_secret': os.environ.get('KAKAO_CLIENT_SECRET'),
            'redirect_uri': os.environ.get('KAKAO_REDIRECT_URI'),
            'code': access_code,
        },
    )
    if response.status_code >= 300:
        raise KakaoAccessTokenException(response.json())
    return response.json()

def get_kakao_user_info(access_token):
    response = requests.get(
        'https://kapi.kakao.com/v2/user/me',
        headers={
            'Authorization': f'Bearer {access_token}',
        },
    )
    if response.status_code >= 300:
        raise KakaoAccessTokenException(response.json())
    return response.json()

def kakao_signup(access_code):            
    try: 
        token_response = exchange_kakao_access_token(access_code)
        access_token = token_response['access_token']
        kakao_user_info = get_kakao_user_info(access_token)
        kakao_id = kakao_user_info['id']
        email = kakao_user_info.get('kakao_account').get('email')
        nickname = kakao_user_info.get('properties').get('nickname')
        # 사용자가 이미 존재하는지 확인
        if User.objects.filter(platformId=kakao_id).exists():
            return Response({'message': '이미 존재하는 회원입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 새로운 사용자 생성
        user = User.objects.create(
            username= nickname + str(kakao_id),
            platformId=kakao_id,
            provider='kakao',
            email=email,
            nickname=nickname,
            number=""
        )
        user.set_unusable_password()  # 소셜 로그인 사용자는 비밀번호를 직접 설정하지 않음
        user.save()
        return user
    except KakaoAccessTokenException as e:
        return Response({'error': 'Failed to obtain access token', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)

def kakao_login(access_code):
    try:
        token_response = exchange_kakao_access_token(access_code)
        access_token = token_response['access_token']
        kakao_user_info = get_kakao_user_info(access_token)
        kakao_id = kakao_user_info['id']
        
        if not User.objects.filter(platformId=kakao_id).exists():
            return Response({'message': '존재하지 않는 유저입니다.'}, status=status.HTTP_404_NOT_FOUND)

        # 회원가입 되어 있는 사용자 -> 로그인
        user = User.objects.get(platformId=kakao_id)
        return user 

    except KakaoAccessTokenException as e:
        return Response({'error': 'Failed to obtain access token', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)


def exchange_naver_access_token(access_code):
    response = requests.post(
        'https://nid.naver.com/oauth2.0/token',
        headers={
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        },
        data={
            'grant_type': 'authorization_code',
            'client_id': os.environ.get('NAVER_REST_API_KEY'),
            'client_secret': os.environ.get('NAVER_CLIENT_SECRET'),
            'redirect_uri': os.environ.get('NAVER_REDIRECT_URI'),
            'code': access_code,
        },
    )
    if response.status_code >= 300:
        raise NaverAccessTokenException(response.json())
    return response.json()

def get_naver_user_info(access_token):
    response = requests.get(
        'https://openapi.naver.com/v1/nid/me',
        headers={
            'Authorization': f'Bearer {access_token}',
        },
    )
    if response.status_code >= 300:
        raise NaverAccessTokenException(response.json())
    return response.json()

def naver_signup(access_code):
    try: 
        token_response = exchange_naver_access_token(access_code)
        access_token = token_response['access_token']
        naver_user_info = get_naver_user_info(access_token)
        naver_id = naver_user_info.get('response').get('id')
        email = naver_user_info.get('response').get('email')
        nickname = naver_user_info.get('response').get('name')
        # 사용자가 이미 존재하는지 확인
        if User.objects.filter(platformId=naver_id).exists():
            return Response({'message': '이미 존재하는 회원입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 새로운 사용자 생성
        user = User.objects.create(
            username= nickname + naver_id,
            platformId=naver_id,
            provider='naver',
            email=email,
            nickname=nickname,
            number=""
        )

        user.set_unusable_password()  # 소셜 로그인 사용자는 비밀번호를 직접 설정하지 않음
        user.save()

        return user
    except NaverAccessTokenException as e:
        return Response({'error': 'Failed to obtain access token', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
def naver_login(access_code):
    try:
        token_response = exchange_naver_access_token(access_code)
        access_token = token_response['access_token']
        naver_user_info = get_naver_user_info(access_token)
        naver_id = naver_user_info.get('response').get('id')
        # 사용자가 존재하는지 확인
        if not User.objects.filter(platformId=naver_id).exists():
            return Response({'message': '존재하지 않는 유저입니다.'}, status=status.HTTP_404_NOT_FOUND)

        # 회원가입 되어 있는 사용자 -> 로그인
        user = User.objects.get(platformId=naver_id)
        
        return user 

    except NaverAccessTokenException as e:
        return Response({'error': 'Failed to obtain access token', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)


def exchange_google_access_token(access_code):
    response = requests.post(
        'https://oauth2.googleapis.com/token',
        headers={
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        },
        data={
            'grantType': 'authorization_code',
            'clientId': os.environ.get('GOOGLE_REST_API_KEY'),
            'clientSecret': os.environ.get('GOOGLE_CLIENT_SECRET'),
            'redirectUri': os.environ.get('GOOGLE_REDIRECT_URI'),
            'code': urllib.parse.unquote(access_code, encoding='utf-8'),
        },
    )
    if response.status_code >= 300:
        raise GoogleAccessTokenException(response.json())
    return response.json()

def get_google_user_info(access_token):
    response = requests.get(
        'https://www.googleapis.com/oauth2/v3/userinfo',
        headers={
            'Authorization': f'Bearer {access_token}',
        },
    )
    if response.status_code >= 300:
        raise GoogleAccessTokenException(response.json())
    return response.json()

def google_signup(access_code):
    try: 
        token_response = exchange_google_access_token(access_code)
        access_token = token_response['access_token']
        google_user_info = get_google_user_info(access_token)
        google_id = google_user_info.get('sub')
        email = google_user_info.get('email')
        nickname = google_user_info.get('name')
        # 사용자가 이미 존재하는지 확인
        if User.objects.filter(platformId=google_id).exists():
            return Response({'message': '이미 존재하는 회원입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 새로운 사용자 생성
        user = User.objects.create(
            username= nickname + google_id,
            platformId=google_id,
            provider='google',
            email=email,
            nickname=nickname,
            number=""
        )

        user.set_unusable_password()  # 소셜 로그인 사용자는 비밀번호를 직접 설정하지 않음
        user.save()
        return user
    except GoogleAccessTokenException as e:
        return Response({'error': 'Failed to obtain access token', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)

def google_login(access_code):
    try:
        token_response = exchange_google_access_token(access_code)
        access_token = token_response['access_token']
        google_user_info = get_google_user_info(access_token)
        google_id = google_user_info.get('sub')

        # 사용자가 존재하는지 확인
        if not User.objects.filter(platformId=google_id).exists():
            return Response({'message': '존재하지 않는 유저입니다.'}, status=status.HTTP_404_NOT_FOUND)

        # 회원가입 되어 있는 사용자 -> 로그인
        user = User.objects.get(platformId=google_id)
        
        return user 

    except GoogleAccessTokenException as e:
        return Response({'error': 'Failed to obtain access token', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)