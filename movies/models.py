from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    category=models.CharField(max_length=50,unique=True)
    slug=models.SlugField(blank=True)
    
    def __str__(self):
        return self.category

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.title)

        super().save(*args,**kwargs)

class Movie(models.Model):
    movie=models.CharField(max_length=100)
    trailer_link=models.URLField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    release_date=models.DateField()
    poster=models.ImageField(upload_to="poster/")
    description=models.TextField()
    user_rating=models.DecimalField(max_digits=3,decimal_places=1)
    actors=models.ManyToManyField(
        "actors.Actors",
        through="Cast",
        related_name="movies",
        blank=True,
    )

    def __str__(self):
        return self.movie
# Create your models here.

class Cast(models.Model):
    movie= models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor= models.ForeignKey("actors.Actors", on_delete=models.CASCADE)
    character_name=models.CharField(max_length=100,blank=True)

    class Meta:
        constraints=[
            models.UniqueConstraint(
                fields=["movie", "actor", "character_name"],
                name="unique_movie_actor_character",
            )
        ]

    def __str__(self):
        return f"{self.actor} in {self.movie}"


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["movie", "user"], name="one_review_per_user_per_movie")
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} on {self.movie}"