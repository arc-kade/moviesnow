from django.urls import path
from movies import views

urlpatterns=[
    path("add-movie/",views.addMovie,name="add-movie"),
    path('all-movies',views.movie_list,name="movie_list")
]