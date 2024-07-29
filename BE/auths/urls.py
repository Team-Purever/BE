from django.urls import path
from .views import signup, refreshToken, login, user_detail

urlpatterns = [
    path('login', login),
    path('signup', signup),
    path('reissue', refreshToken),
    path('user/info', user_detail),
]