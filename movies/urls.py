from django.urls import path
from movies import views

urlpatterns=[
    path("",views.home,name="index"),
    path("add-movie/",views.addMovie,name="add-movies"),
    path('all-movies/',views.movie_list,name="all-movies"),
    path("update-movie/<int:movie_id>/",views.updateMovie,name="update-movie"),
    path("details/<int:movie_id>/",views.viewMovie,name="movie-detail")
]