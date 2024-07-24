from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Pet
from .serializers import PetSerializer

class PetList(ListCreateAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

class PetDetail(RetrieveUpdateDestroyAPIView):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

