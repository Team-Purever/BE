from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from .models import Place
from .serializers import PlaceSerializer

class PlaceList(APIView):
    permission_classes = [IsAuthenticated]
    # 웰다잉 플레이스 조회
    def get(self, request, *args, **kwargs):
        city = request.query_params.get('city')
        category = request.query_params.get('category')
        
        queryset = Place.objects.all()
        if city:
            queryset = queryset.filter(city__icontains=city)
        if category:
            queryset = queryset.filter(category__icontains=category)

        paginator = PageNumberPagination()
        paginator.page_size = 6
        places = paginator.paginate_queryset(queryset, request)
        serializer = PlaceSerializer(places, many=True)
        serialized_data = [
            {
                "id": place['id'],
                "name": place['name'],
                "address": place['address'],
                "number": place['number'],
                "url": place['url'],
                "imgUrl": place['imgUrl']    
            } for place in serializer.data
        ]
        return paginator.get_paginated_response({
            "status": 200,
            "message": "웰다잉 플레이스 조회 완료.",
            "data": serialized_data
        })


class PlaceRegister(APIView):   
    permission_classes = [AllowAny] 
    # 웰다잉 플레이스 등록
    def post(self, request):
        serializer = PlaceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class PlaceDetail(APIView):
    permission_classes = [AllowAny]
    def get_object(request, pk):
        place = get_object_or_404(Place, pk=pk)
        return place

    def get(self, request, pk):
        place = self.get_object(pk)
        serializer = PlaceSerializer(place)
        return Response(serializer.data)

    def patch(self, request, pk):
        place = self.get_object(pk)
        serializer = PlaceSerializer(place, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        place = self.get_object(pk)
        place.delete()
        return Response(status=status.HTTP_200_OK)