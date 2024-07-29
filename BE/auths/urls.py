from django.urls import path, include
from auths.views import signup, refreshToken, login, user_detail

urlpatterns = [
    path('login/', login),
    path('signup/', signup),
    path('reissue/', refreshToken),
    path('user/info', user_detail),
]
