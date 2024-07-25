from django.urls import path, include
# from watchlist_app.api.views import movie_list, movie_details
from auths.views import signup, refreshToken, login

urlpatterns = [
    path('login/', login),
    path('signup/', signup),
    path('reissue/', refreshToken),
]
