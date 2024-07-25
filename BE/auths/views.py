from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .models import User
from .serializers import UserSerializer
from .utils import kakao_signup, kakao_login, google_signup, google_login, naver_signup, naver_login, KakaoAccessTokenException, NaverAccessTokenException,GoogleAccessTokenException
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
# Create your views here.

# 회원가입
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    access_code = request.headers.get('Authorization')
    if not access_code:
        return Response({'message': '코드 에러'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        platform = request.data.get("platform")
        if platform == "kakao":
            user =  kakao_signup(access_code)
        elif platform == "google":
            user = google_signup(access_code)
        elif platform == "naver":   
            user = naver_signup(access_code)
        
        # JWT 토큰 발급
        refresh = RefreshToken.for_user(user)
        return Response({
            'status': 201,
            'message': '회원가입이 완료되었습니다.',
            'data': {
                 'refreshToken': str(refresh),
                 'accessToken': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    except KakaoAccessTokenException | NaverAccessTokenException | GoogleAccessTokenException as e:
        return Response({'error': 'Failed to obtain access token', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# 회원가입
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    access_code = request.headers.get('Authorization')
    if not access_code:
        return Response({'message': '코드 에러'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        platform = request.data.get("platform")
        if platform == "kakao":
            user =  kakao_login(access_code)
        elif platform == "google":
            user = google_login(access_code)
        elif platform == "naver":   
            user = naver_login(access_code)
        
        # JWT 토큰 발급
        refresh = RefreshToken.for_user(user)
        return Response({
            'status': 200,
            'message': "로그인에 성공했습니다.",
            'data': {
                 'refreshToken': str(refresh),
                 'accessToken': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    except KakaoAccessTokenException | NaverAccessTokenException | GoogleAccessTokenException as e:
        return Response({'error': 'Failed to obtain access token', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def refreshToken(request):
    # Authorization 헤더에서 토큰을 추출
    auth_header = request.headers.get('refreshToken')
    if not auth_header:
        return Response({'error': 'Authorization header not found'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        # "Bearer <token>" 형식의 헤더에서 토큰만 추출
        _, token = auth_header.split()
    except ValueError:
        return Response({'error': 'Invalid Authorization header format'}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        refresh_token = RefreshToken(token)
    except Exception as e:
        return Response({'error': 'Invalid token', 'details': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
    # 토큰에서 payload (예. user_id 등)에 접근
    user_id = refresh_token['user_id']
    user = User.objects.get(pk=user_id)
    refresh = RefreshToken.for_user(user)
    return Response({
        'status': 200,
        'message': '정상 요청 완료.',
        'data': {
                'refreshToken': str(refresh),
                'accessToken': str(refresh.access_token),
        }
    }, status=status.HTTP_201_CREATED)
  
