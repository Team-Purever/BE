from django.urls import path
from .views import PetList, PetDetail

urlpatterns = [
    path('pets', PetList.as_view()),
    path('pets/<int:pk>', PetDetail.as_view()),
]