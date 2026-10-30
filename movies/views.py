from django.shortcuts import render,redirect
from movies.models import Category,Movie
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request,"index.html")

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

def updateMovie(request,movie_id):
    categories = Category.objects.all()
    movie=Movie.objects.get(id=movie_id)
    if request.method=="POST":
        movie_name=request.POST["movie"]
        tr_link=request.POST["trailer_link"]
        cate = request.POST["category"]
        category=Category.objects.get(id=cate)
        re_date=request.POST["release_date"]
        if "poster" in request.FILES:
            poster = request.FILES["poster"]
            movie.poster = poster
        desc = request.POST["description"]
        rating = request.POST["rating"]
        movie.movie=movie_name
        movie.trailer_link=tr_link
        movie.category=category
        movie.release_date=re_date
        movie.description=desc
        movie.rating=rating
        movie.save()
        return redirect("movie-detail",movie_id)
    return render(request, "update-movie.html",{"movie":movie,"categories":categories})

def viewMovie(request,movie_id):
    my_movie=Movie.objects.get(id=movie_id)
    return render(request, "movie-detail.html",{"movie":my_movie})
# Create your views here.


