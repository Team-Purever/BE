from django.urls import path, include
# from watchlist_app.api.views import movie_list, movie_details
from diaries.views import img_create, diary_create, diary_edit

urlpatterns = [
    path('pets/img/', img_create),
    path('pets/<int:petId>/', diary_create),
    path('<int:diairyId>/', diary_edit),
]
