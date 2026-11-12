from django.urls import path
from actors import views

urlpatterns=[
    path("add-actor/",views.AddActor.as_view(),name="add_actor"),
    path("all-actors/",views.AllActors.as_view(),name="actors_list")
]