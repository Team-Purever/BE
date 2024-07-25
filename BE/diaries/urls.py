from django.urls import path, include
# from watchlist_app.api.views import movie_list, movie_details
from diaries.views import img_create

urlpatterns = [
    path('pets/img/', img_create),

]
