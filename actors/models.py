from django.db import models

# Create your models here.
class Actors(models.Model):
    name=models.CharField(max_length=40)
    dob=models.DateField(auto_now_add=False)
    country=models.CharField(max_length=20)
    portrait= models.ImageField(upload_to='portrait/')
    about=models.TextField()