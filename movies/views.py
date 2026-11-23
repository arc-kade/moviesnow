from django.shortcuts import render,redirect,get_object_or_404
from movies.models import Category,Movie,Cast, Review
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from actors.models import Actors
from django.db.models import Avg,Count
from accounts.decorators import superuser_required
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


@superuser_required
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
            editor_rating=request.POST["editor_rating"],
        )
        new_movie.save()
        save_cast(new_movie,request.POST)
        return redirect("all-movies")
    return render(request,"add-movies.html", 
                  {"categories":Category.objects.all(),
                   "actors":Actors.objects.all(),
                   "existing_cast":[]})

def movie_list(request):
    movies = Movie.objects.annotate(
        avg_rating=Avg("reviews__rating"),
        review_count=Count("reviews"),
    )
    actor_id=request.GET.get("actor")
    selected_actor = None
    if actor_id:
        movies = movies.filter(pk__in=Cast.objects.filter(actor_id=actor_id).values("movie_id"))
        selected_actor=Actors.objects.filter(id=actor_id).values("movie_id")
    return render(request,'all-movies.html',{
        'movies':movies, 
        'actors':Actors.objects.all(), 
        'selected_actor':selected_actor,
        })

def category_movies(request,slug):
    category=get_object_or_404(Category,slug=slug)
    movies=Movie.objects.filter(category=category).annotate(
        avg_rating=Avg("reviews__rating"),
        review_count=Count("reviews"),
    )
    return render(request,'all-movies.html',
                  {"movies":movies,
                   "selected_category":category, 
                   "actors":Actors.objects.all(),},
    )

@superuser_required
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
        movie.editor_rating = request.POST["editor_rating"]
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
    
    my_movie= Movie.objects.filter(id=movie_id).first()
    cast= (
        Cast.objects.filter(movie=my_movie).select_related("actor")
        if my_movie else []
    )
    reviews=my_movie.reviews.select_related("user") if my_movie else []
    user_review=reviews.filter(user=request.user).first() if my_movie else[]
    
    return render(request, "movie-detail.html",{
        "movie":my_movie,
        "cast":cast,
        "reviews":reviews,
        "user_review":user_review,},)

@superuser_required
def deleteMovie(request,movie_id):
    movie=Movie.objects.get(id=movie_id)
    movie.delete()
    return redirect(movie_list)


# Create your views here.


@login_required(login_url="login")
@require_POST
def add_review(request,movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    try:
        rating=int(request.POST.get("rating",""))
    except ValueError:
        return redirect("movie-detail",movie_id)
    if not 1<= rating <=10:
        return redirect("movie-detail",movie_id)

    Review.objects.update_or_create(
        movie=movie,
        user=request.user,
        defaults={"rating":rating,"comment":request.POST.get("comment","").strip()},
    )
    return redirect("movie-detail", movie_id)

@login_required(login_url="login")
@require_POST
def delete_review(request,review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user_id==request.user.id or request.user.is_staff:
        review.delete()
    return redirect("movie-detail",review.movie_id)
