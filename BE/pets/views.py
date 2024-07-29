from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from .models import Pet, PetImg
from .serializers import PetSerializer, PetImgSerializer
from auths.models import User

class PetList(APIView):
    permission_classes = [IsAuthenticated]
    # 전체 반려동물 조회
    def get(self, request):
        auth_header = request.headers.get('Authorization')
        _, token = auth_header.split()
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        
        user = User.objects.get(pk=user_id)
        pets = Pet.objects.filter(user=user)
        serializer = PetSerializer(pets, many=True)
        serialized_data = [
            {
                "petId": pet['id'],
                "name": pet['name'],
                "url": pet['url']
            } for pet in serializer.data
        ]
        return Response({
            "status": 200,
            "message": "반려동물 조회 완료.",
            "data": {
                "Pets": serialized_data
            }
        })
    
    # 반려동물 등록
    def post(self, request):
        auth_header = request.headers.get('Authorization')
        _, token = auth_header.split()
        access_token = AccessToken(token)
        user_id = access_token['user_id']
    
        user = User.objects.get(pk=user_id)
        serializer = PetSerializer(data=request.data)
        if serializer.is_valid():
            pet = Pet.objects.create(
                user = user,
                name = serializer.validated_data['name'],
                age = serializer.validated_data['age'],
                url = serializer.validated_data['url'],
            )
            return Response({
                "status": 201,
                "message": "반려동물 등록 완료.",
                "data": {
                    "petId": pet.id
                }    
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class PetDetail(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(request, pk):
        pet = get_object_or_404(Pet, pk=pk)
        return pet

    # 개별 반려동물 조회
    def get(self, request, pk):
        auth_header = request.headers.get('Authorization')
        _, token = auth_header.split()
        access_token = AccessToken(token)
        user_id = access_token['user_id']

        user = User.objects.get(pk=user_id)
        pet = self.get_object(pk)

        if pet.user == user:
            serializer = PetSerializer(pet)
            return Response({
                "status": 200,
                "message": "반려동물 조회 완료.",
                "data": {
                    "pet": {
                        "petId": serializer.data['id'],
                        "name": serializer.data['name'],
                        "url": serializer.data['url']
                    }
                }    
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": 403,
                "message": "해당 반려동물 조회 권한이 없습니다."
            }, status=status.HTTP_403_FORBIDDEN)

    # 반려동물 정보 수정
    def patch(self, request, pk):
        auth_header = request.headers.get('Authorization')
        _, token = auth_header.split()
        access_token = AccessToken(token)
        user_id = access_token['user_id']

        user = User.objects.get(pk=user_id)
        pet = self.get_object(pk)

        if pet.user == user:
            serializer = PetSerializer(pet, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({
                    "status": 200,
                    "message": "반려동물 정보 수정 완료.",
                    "data": {
                        "pet": {
                            "petId": serializer.data['id'],
                            "name": serializer.data['name'],
                            "url": serializer.data['url']
                        }
                    }    
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "status": 403,
                "message": "해당 반려동물 수정 권한이 없습니다."
            }, status=status.HTTP_403_FORBIDDEN)
    
    # 반려동물 삭제
    def delete(self, request, pk):
        auth_header = request.headers.get('Authorization')
        _, token = auth_header.split()
        access_token = AccessToken(token)
        user_id = access_token['user_id']

        user = User.objects.get(pk=user_id)
        pet = self.get_object(pk)

        if pet.user == user:
            pet.delete()
            return Response({
                "status": 200,
                "message": "반려동물 삭제 완료.",
                "data": {}    
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": 403,
                "message": "해당 반려동물 삭제 권한이 없습니다."
            }, status=status.HTTP_403_FORBIDDEN)


# 반려동물 사진 등록
class PetImgRegister(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = PetImgSerializer(data=request.data)
        try: 

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({
                    "status": 201,
                    "message": "반려동물 사진 등록 완료.",
                    "data": {
                        "url": serializer.data['url']
                    }
                }, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)