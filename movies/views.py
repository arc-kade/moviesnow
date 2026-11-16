from django.shortcuts import render,redirect,get_object_or_404
from movies.models import Category,Movie,Cast
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from actors.models import Actors
# Create your views here.

def home(request):
    return render(request,"index.html")

def save_cast(movie,post):
    movie.cast_set.all().delete()
    actor_ids = post.getlist("cast_actor")
    characters = post.getlist("cast_character")
    valid = {
        str(i)
        for i in Actors.objects.filter(
            id__in=[a for a in actor_ids if a]
        ).values_list("id",flat=True)
    }
    seen, rows = set(), []
    for aid, ch, in zip(actor_ids,characters):
        ch = ch.strip()
        if aid in valid and (aid,ch) not in seen:
            seen.add((aid,ch))
            rows.append(Cast(movie=movie, actor_id=aid,character_name=ch))
    Cast.objects.bulk_create(rows)


@login_required(login_url="login")
def addMovie(request):
    if request.method=="POST":
        category=Category.objects.get(id=request.POST["category"])
        new_movie = Movie(
            movie=request.POST["movie"],
            trailer=request.POST["trailer_link"],
            category=category,
            release_date=request.POST["release_date"],
            poster=request.FILES["poster"],
            desc=request.POST["description"],
            rating=request.POST["rating"],
        )
        new_movie.save()
        save_cast(new_movie,request.POST)
        return redirect("all-movies")
    return render(request,"add-movies.html", 
                  {"categories":Category.objects.all(),
                   "actors":Actors.objects.all(),
                   "existing_cast":[]})

def movie_list(request):
    movies = Movie.objects.all()
    actor_id=request.GET.get("actor")
    selected_actor = None
    if actor_id:
        movies = movies.filter(actors__id=actor_id)
        selected_actor = Actors.objects.filter(id=actor_id).first()
    return render(request,'all-movies.html',{'movies':movies, 'actors':Actors.objects.all(), 'selected_actor':selected_actor,})

def category_movies(request,slug):
    category=get_object_or_404(Category,slug=slug)
    movies=Movie.objects.filter(category=category)
    return render(
        request,'all-movies.html',{"movies":movies,"selected_category":category, "actors":Actors.objects.all()},
    )

@login_required(login_url="login")
def updateMovie(request,movie_id):
    categories = Category.objects.all()
    movie=get_object_or_404(Movie,id=movie_id)
    if request.method=="POST":
        movie.movie=request.POST["movie"]
        movie.trailer_link=request.POST["trailer_link"]
        cate = request.POST["category"]
        movie.category=Category.objects.get(id=cate)
        movie.release_date=request.POST["release_date"]
        if "poster" in request.FILES:
            movie.poster = request.FILES["poster"]
        movie.description = request.POST["description"]
        movie.rating = request.POST["rating"]
        movie.save()
        save_cast(movie,request.POST)
        return redirect("movie-detail",movie_id)
    return render(request, "update-movie.html",{
        "movie":movie,
        "categories":categories,
        "actors":Actors.objects.all(),
        "existing_cast":Cast.objects.filter(movie=movie)})

@login_required(login_url="login")
def viewMovie(request,movie_id):
    try:
        my_movie= Movie.objects.filter(id=movie_id).first()
        cast= (
            Cast.objects.filter(movie=my_movie).select_related("actor")
            if my_movie else []
        )
        
    except Movie.DoesNotExist:
        my_movie=None
    
    return render(request, "movie-detail.html",{"movie":my_movie,"cast":cast})


def deleteMovie(request,movie_id):
    movie=Movie.objects.get(id=movie_id)
    movie.delete()
    return redirect(movie_list)


# Create your views here.


