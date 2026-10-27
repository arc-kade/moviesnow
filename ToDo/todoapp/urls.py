from django.urls import path
from todoapp import views




urlpatterns = [
    path('',views.Home,name="home"),
    path('edit-task/<int:task_id>/',views.editTask,name="edit"),
    path('delete-task/<int:task_id>/',views.deleteTask,name="delete"),
    path('about-me/',views.About,name="about"),
    path('contact-us/',views.Contact,name="contact")
]