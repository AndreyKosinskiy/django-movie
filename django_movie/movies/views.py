from django.shortcuts import render
from django.views.generic import View
from .models import Movie
# Create your views here.

class MovieViews(View):
    """ Вывов списка фильмов """
    def get(self,request):
        movies = Movie.objects.all()
        return render(request,'movies/movies.html',{'movie_list':movies})
