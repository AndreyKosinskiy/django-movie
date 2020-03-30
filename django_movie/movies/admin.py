from django.contrib import admin
from .models import Actor, Category, Genre, Movie, RatingStar, Reviews, Rating, MovieShots
# Register your models here.
admin.site.register(Actor)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(RatingStar)
admin.site.register(Reviews)
admin.site.register(Rating)
admin.site.register(MovieShots)