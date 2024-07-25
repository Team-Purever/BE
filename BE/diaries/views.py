from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ImageSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
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
