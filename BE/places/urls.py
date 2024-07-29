from django.urls import path
from .views import PlaceList, PlaceRegister, PlaceDetail

urlpatterns = [
    path('', PlaceList.as_view()),
    path('register', PlaceRegister.as_view()),
    path('<int:pk>', PlaceDetail.as_view()),
]