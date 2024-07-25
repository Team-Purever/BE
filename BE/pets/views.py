from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Pet
from .serializers import PetSerializer

"""
class PetList(ListCreateAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

class PetDetail(RetrieveUpdateDestroyAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
"""

class PetList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        pets = Pet.objects.all()
        serializer = PetSerializer(pets, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PetDetail(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(request, pk):
        pet = get_object_or_404(Pet, pk=pk)
        return pet

    def get(self, request, pk):
        pet = self.get_object(pk)
        serializer = PetSerializer(pet)
        return Response(serializer.data)

    def patch(self, request, pk):
        pet = self.get_object(pk)
        serializer = PetSerializer(pet, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        pet = self.get_object(pk)
        pet.delete()
        return Response(status=status.HTTP_200_OK)
