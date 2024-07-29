from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ImageSerializer, DiraySerializer, DiraySerializer2
from .models import Diary
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from auths.models import User
from pets.models import Pet
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def img_create(request):
    serializers = ImageSerializer(data=request.data) # 꼭 !!!! files는 따로 request의 FILES로 속성을 지정해줘야 함
    if serializers.is_valid():
        serializers.save()
        return Response({
            'status': 201,
            'message': "반려동물 추억일기장 사진 등록 성공.",
            'data': {
                 'url': serializers.data.get('url'),
            }
        }, status=status.HTTP_201_CREATED)
    else:
        return Response("실패!")

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def diary_create(request, petId):
    auth_header = request.headers.get('Authorization')
    _, token = auth_header.split()
    access_token = AccessToken(token)

    # if not Pet.objects.filter(pk=petId).exists():
    #         return Response({'message': '존재하지 않는 petId 입니다..'}, status=status.HTTP_400_BAD_REQUEST)

    user_id = access_token['user_id']
    user = User.objects.get(pk=user_id)
        
    Diary.objects.create(
            user= user,
            pet_id=petId,
            title=request.data.get('title'),
            content=request.data.get('content'),
            url=request.data.get('url'),
    )
    return Response({
            'status': 201,
            'message': "추억 일기장 작성 완료.",
            'data': {}
            
        }, status=status.HTTP_201_CREATED)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def diary_edit(request, diairyId):

    if not Diary.objects.filter(pk=diairyId).exists():
            return Response({'message': '존재하지 않는 diaryId 입니다.'}, status=status.HTTP_404_BAD_REQUEST)

    diary = Diary.objects.get(pk=diairyId)
    

    diary.url = request.data.get('url')
    diary.content = request.data.get('content')
    diary.save()
    return Response({
                'status': 200,
                'message': "추억 일기장 수정 완료.",
                'data': {}
            }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_diary(request, petId):

    auth_header = request.headers.get('Authorization')
    _, token = auth_header.split()
    access_token = AccessToken(token)

    # if not Pet.objects.filter(pk=petId).exists():
    #         return Response({'message': '존재하지 않는 petId 입니다..'}, status=status.HTTP_404_NOT_FOUND)
    #
    #  팻조회 필요
    #
    user_id = access_token['user_id']
    user = User.objects.get(pk=user_id)

    diaries = Diary.objects.filter(user=user, pet_id=petId)
    serializer = DiraySerializer2(diaries, many=True)
    
    response_diaires = serializer.data 

    response_diaires.sort(key = lambda x: x.get('created_at'))
    response_diaires.reverse()
    return Response({
                'status': 200,
                'message': "반려동물 추억 일기장 조회 완료.",
                'data': {
                           "name": "태백이",
                            "age": 12,
                             "url": "/img/filename.jpg",
                             "diaries": response_diaires

                }
            }, status=status.HTTP_200_OK)
    return Response(serializer.data)
    
    