from django.shortcuts import render,redirect
from movies.models import Category,Movie
from django.http import HttpResponse
# Create your views here.


def addMovie(request):
    if request.method=="POST":
        movie=request.POST["movie"]
        trailer=request.POST["trailer_link"]
        cate=request.POST["category"]
        category=Category.objects.get(id=cate)
        release_date=request.POST["release_date"]
        poster=request.FILES["poster"]
        desc=request.POST["description"]
        rating=request.POST["rating"]
        Movie(movie=movie,trailer_link=trailer,category=category,release_date=release_date,poster=poster,description=desc,rating=rating).save()
        return redirect("all-movies")
    categories=Category.objects.all()
    return render(request,"add-movies.html",{"categories":categories})

def movie_list(request):
    movies = Movie.objects.all()
    return render(request,'all-movies.html',{'movies':movies})


# Create your views here.


